# A deep read of the AutomationExercise framework

`readme.md` is the reference: what each directory holds, how to run it, every
flag. This is the other document, the one that explains *why* it is shaped this
way, what the interesting problems were, and which bits I would defend in a
review.

It is written for someone who has to work in the code, or who is deciding
whether the approach is worth copying.

- [1. What it is](#1-what-it-is)
- [2. The layering rule](#2-the-layering-rule)
- [3. One test, all the way down](#3-one-test-all-the-way-down)
- [4. Every directory, and its job](#4-every-directory-and-its-job)
- [5. The shared services](#5-the-shared-services)
- [6. The fixtures](#6-the-fixtures)
- [7. The API side](#7-the-api-side)
- [8. Three-tier validation](#8-three-tier-validation)
- [9. Evidence](#9-evidence)
- [10. Running in parallel, and the bug it caused](#10-running-in-parallel-and-the-bug-it-caused)
- [11. Telling flakiness apart from failure](#11-telling-flakiness-apart-from-failure)
- [12. Configuration](#12-configuration)
- [13. CI](#13-ci)
- [14. Running it yourself](#14-running-it-yourself)
- [15. Bugs worth knowing about](#15-bugs-worth-knowing-about)
- [16. What is still wrong with it](#16-what-is-still-wrong-with-it)
- [17. FAQ](#17-faq)

---

## 1. What it is

### If you do not write software

Websites break. Not usually in dramatic ways: a button moves, a form stops
saving, a price displays wrong for one currency. A person could click through
every page after every change to check, and on a real product that is hours a
day, so nobody does it, and things ship broken.

This is a program that does the clicking. Thirty of them, actually: thirteen that
open a real browser and go through the site the way a person would (register,
log in, search, add to a cart, check out, pay), and seventeen that talk to the
server directly, faster, to check it is answering correctly.

They run automatically every time the code changes, in about two minutes, and
they publish a report anyone can open. When one fails, it does not just say
"failed": it hands you a recording of exactly what the browser did, which you can
replay step by step.

### If you write software

A Python and Playwright framework covering UI and API, layered so that a test
reads as intent and never touches a selector, with everything expensive behind
fixtures.

```python
def test_login_user(page, registered_user):
    home = HomePage(page)
    signup_login = home.navbar.open_signup_login()
    signup_login.login(registered_user.email, registered_user.password)
    assert home.user_logged_in()
```

Six lines, no URL, no selector, no wait, no browser setup. That is the whole
point of the structure, and [section 3](#3-one-test-all-the-way-down) traces
that exact test down through every layer it touches.

Thirty tests, run with `pytest -n 2` inside Docker, publishing an Allure report
with trend history to GitHub Pages on every push.

### If you are reviewing the design

Four things are worth your time.

**The one-way dependency rule** ([section 2](#2-the-layering-rule)), which is
what makes a failure locate itself before you open anything.

**The shared execution id** ([section 10](#10-running-in-parallel-and-the-bug-it-caused)),
which is a small fix for a bug that could publish a green report over a
half-empty run.

**Three-tier API validation** ([section 8](#8-three-tier-validation)), because a
200 carrying the wrong body should not pass.

**Telling flakiness apart from failure** ([section 11](#11-telling-flakiness-apart-from-failure)),
which is most of what makes a suite against a public practice site usable at all.

---

## 2. The layering rule

> **A layer may call downwards. It may never call upwards or sideways.**

```
tests/          may call flows              assertions, and nothing else
flows/          may call pages and clients  multi-step journeys, no assertions
pages/  api/    may call services           every selector and endpoint
utils/          calls nothing above         config, browsers, auth, artifacts
```

That is the entire rule, and it is worth being pedantic about, because the value
only arrives when there are no exceptions.

The payoff is not tidiness. It is that **a failure tells you which layer to open
before you have read anything**:

| What went red | Where it is | Why it can only be there |
|---|---|---|
| An assertion failed | `tests/` | Assertions live nowhere else, so either the expectation is stale or the product is genuinely broken |
| Timed out waiting for an element | `pages/` | Selectors live in exactly one layer, and the screenshot is already attached |
| Half the suite failed at the same step | `flows/` | A shared journey broke. One fix, not fifteen, and the failure *count* is what tells you |
| A response no longer matches its schema | `schemas/` | Contract validation runs on every API response |
| Everything failed before the first test | `conftest.py` | Setup, not product. Pytest reports a fixture error separately from a test failure |

That last row is a real distinction and it is easy to lose. *The environment is
wrong* and *the code is wrong* are different problems, and pytest already
separates them if you put setup in fixtures rather than at the top of tests.

The rule that costs the most to keep is **flows never assert**. It is tempting:
you are already in `register_and_verify_user`, you already have the response,
just assert there. But a flow that asserts is a test pretending to be a helper,
and when it fails the report blames the wrong thing. The API flows here do
assert, which is an exception I explain and half-defend in
[section 8](#8-three-tier-validation).

---

## 3. One test, all the way down

`tests/UI/test_login.py`:

```python
@allure.title("Login with valid credentials")
@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.smoke
def test_login_user(page, registered_user):
    home = HomePage(page)
    signup_login = home.navbar.open_signup_login()
    signup_login.login(registered_user.email, registered_user.password)
    assert home.user_logged_in()
```

**Step 1: what the test asked for.** `page` and `registered_user`. It does not
know that `page` came from a factory that read an env file to decide Chromium and
headless, opened a context with video recording and tracing on, and applied the
configured timeout. It does not know `registered_user` was created over the API
because doing it through the UI would cost fifteen seconds a test.

**Step 2: the page object.** `pages/signup_login_page/signup_login_page.py`:

```python
self._login_email    = page.locator("[data-qa='login-email']")
self._login_password = page.locator("[data-qa='login-password']")
self._login_button   = page.locator("[data-qa='login-button']")

def login(self, email, password) -> HomePage:
    self._fill_login_email(email)
    self._fill_login_password(password)
    self._click_login_button()
    home = HomePage(self.page)
    home.is_loaded()
    return home
```

Two things here do real work.

Selectors are attributes set once in `__init__`, not strings scattered through
methods. A redesign of this screen is one constructor to edit.

`login()` **returns the page you end up on**. That return is what lets the test
read as a journey without ever naming a navigation. `home.navbar.open_signup_login()`
returns a `SignUpLoginPage`; `.login(...)` returns a `HomePage`. The test chains
through the app and the type of each step says where you are.

**Step 3: the base page.** `pages/base_page.py`:

```python
def click(self, locator, description):
    self.wait_for_visibility(locator, description)
    return self._execute_action(
        action=lambda: locator.click(),
        operation="Click",
        locator=locator,
        description=description,
    )
```

Nobody calls Playwright directly. Every interaction goes through
`_execute_action`, which is why waiting, logging and screenshot-on-failure are
consistent across a hundred call sites instead of being remembered ninety-four
times.

`description` is not decoration. It is what turns a failure into
`Failed Click: Login Button` instead of a locator string nobody can read at a
glance, and it is what the screenshot gets named after.

There is a subtlety in `_execute_action` worth pointing at:

```python
except Exception as e:
    logger.exception(f"Failed {operation} on {description} [{locator}]")
    # Actions nest, so the same exception passes through here more than once.
    # Capture the first (innermost) failure only.
    if not getattr(e, "_screenshot_taken", False):
        self.screenshot(f"Failed {operation}_{...}")
        e._screenshot_taken = True
    raise
```

`click` calls `wait_for_visibility`, which is itself an `_execute_action`. So one
failing click unwinds through the handler twice, and without the flag you get two
screenshots of the same moment, the second one less useful than the first because
it is one frame later and named after the outer operation. Tagging the exception
means the screenshot is of the innermost thing that actually broke.

---

## 4. Every directory, and its job

```
tests/          UI/ and api/            what is being checked
flows/          UI_Flow/ API_Flow/      journeys more than one test needs
pages/          + components/           every selector, one file per screen
api/            client, endpoints, per-resource APIs
models/         request and response dataclasses
schemas/        JSON Schema contracts
utils/          config, browsers, auth, artifacts, readers, writers, logging
config/         default.env + qa/uat/prod.env, credentials
test_data/      users, payments, API payloads
conftest.py     every fixture, and the collection hooks
```

`components/` is the part people miss. A navbar or a cart modal is not a page and
does not deserve a page object, but it is also not nothing: it appears on eight
screens and has its own selectors. `HomePage` exposes `self.navbar`, so
`home.navbar.open_signup_login()` works from anywhere without every page object
redeclaring the navbar's selectors.

`models/` splits by API because there are two under test: `AutomationExercise_UI_API_Models`
and `DummyJsonAPIModels`. Two APIs with different shapes should not share a
`User` class just because both call it a user.

---

## 5. The shared services

All singletons, all reached through fixtures, none of which a test ever
constructs.

### `config_manager`

Reads `config/default.env`, then the per-environment file on top, then real
environment variables on top of that. Common settings live in one file and the
per-environment file only lists what differs, so `qa.env` is four lines rather
than a copy of everything.

It has a `configure()` method rather than a second constructor:

```python
def configure(self, env=None, browser=None):
    # Called from pytest_configure so --environment / --browser actually take effect.
    # Everything imports the singleton at module load, so we reload in place rather
    # than building a second instance.
```

That comment is the whole problem with singletons in one sentence. Every module
does `from utils.config_manager import config` at import time, which happens
before pytest has parsed its command line. Building a second instance would
leave every module holding the first. Reloading in place is the fix, and it is
the kind of thing that is obvious once and mystifying a year later.

### `browser_factory`

Turns config into a launched browser. Chromium, Firefox or WebKit; headless or
not. One session-scoped browser for the whole run, a fresh context per test.

That split is deliberate and it is the standard one: launching a browser is
expensive and a context is cheap, and a context is the real isolation boundary
(its own cookies, its own storage). Sharing a browser and isolating by context
gives you both speed and independence.

### `authentication_manager`

Logs in once per run and hands out the storage state, so tests that need a
logged-in user do not each pay for a login.

```python
# Under xdist two workers can land here together. Write to a process-unique
# file and rename, so nobody ever reads a half-written state.
partial = storage_state.with_name(f"{role}.{os.getpid()}.partial")
context.storage_state(path=partial)
partial.replace(storage_state)
```

Write-to-temp-then-rename, because `rename` is atomic on the same filesystem. Two
workers reaching this together is not hypothetical, and the failure mode without
it is a context loading a truncated JSON file, which surfaces as an unrelated
error somewhere else entirely.

### `artifact_manager`

One folder per run, all of it keyed on a shared execution id.
[Section 10](#10-running-in-parallel-and-the-bug-it-caused) is about why.

---

## 6. The fixtures

The chain for a UI test:

```
playwright   session   the engine, started once
  browser    session   one launched browser
    context  function  fresh cookies, video, tracing, timeouts
      page   function  a new page, already navigated to base_url
```

Session scope on `browser`, function scope on `context`. Every test gets a clean
slate without paying to relaunch a browser thirteen times.

`_apply_timeouts` carries the best comment in the repository, because it
describes a bug that had been invisible for a long time:

```python
"""Make DEFAULT_TIMEOUT mean something.

It was read from config, validated, tuned per environment (uat 30s, prod 60s)
and written into the Allure environment panel, and nothing ever applied it.
"""
```

The setting existed. It was parsed, validated, tuned per environment, and
displayed in the report. It was never passed to Playwright. So every action was
waiting the built-in 30 seconds, the report *advertised* a 10 second timeout the
run did not use, and a genuine failure took three times longer to surface than it
should have.

Nothing errored. Nothing was red. The report was confidently wrong about its own
configuration, which is the failure mode this whole codebase keeps running into
and keeps trying to design against.

Setting it on the context covers every page made from it and every action on
those pages. `expect()` is a separate timeout and is set once in
`pytest_configure`, because it does not inherit from the context.

---

## 7. The API side

Two APIs under test: automationexercise.com's own, and DummyJSON.

`api/api_client.py` wraps Playwright's `APIRequestContext` rather than
`requests`, so UI and API tests share one HTTP stack and one proxy configuration.
Two pieces of behaviour live in it.

**Retry 429 and 5xx, never 4xx.**

```python
retryable = response.status == 429 or response.status >= 500
```

Same reasoning as everywhere else in these repositories: a rate limit from a
shared CI runner is a fact of the environment, and a 4xx is a real answer that
six negative tests assert on. Retrying a 404 would make those tests take four
times as long and still pass, while quietly hiding whether the API is
*consistently* rejecting.

**Reject a non-JSON body outright.** `_reject_non_json` exists because the
practice site sits behind Cloudflare, which under load answers with an HTML
challenge page and a 200. Without this, `response.json()` throws somewhere deep
in a flow and the failure reads as a product defect. It is not; it is a bot
check. Naming it at the client boundary means the report says so.

`endpoints.py` holds the paths, so a path change is one edit. `HttpMethod` is a
`StrEnum`, which is where the framework's Python 3.11 floor comes from.

---

## 8. Three-tier validation

Every API check does three things in order, and the order matters:

```python
with allure.step("Validating HTTP Response"):
    assert response.status == 200                       # 1. transport

with allure.step("Validating business response"):
    assert register_body.responseCode == 201            # 2. the app's own view
    assert register_body.message == "User created!"

with allure.step("Validating JSON Schema"):
    SchemaValidator.validate_response(                  # 3. the contract
        response, "auth/create_user_schema.json")
```

The site is a good teacher here, because it returns HTTP 200 with a *body* that
says `responseCode: 400`. Checking only the status code would pass a request that
the application itself considers a failure. Checking only the body would miss a
502. Checking neither shape means a renamed field ships green.

Tier 3 is the one people skip, and it is the one that catches a backend team
renaming `firstName` to `first_name`: status still 200, business code still 201,
schema fails.

**The exception to the layering rule.** These assertions are in `flows/`, not
`tests/`. That contradicts [section 2](#2-the-layering-rule) and I want to be
straight about it rather than pretend it is consistent.

The argument for: the three tiers are one indivisible act of "did this API call
succeed", they are identical for every caller, and a test that repeated all three
for every endpoint would be mostly copy-paste.

The argument against: when `register_and_verify_user` fails, the report blames a
flow, and a reader has to open it to find out which of the three tiers broke. The
Allure steps recover most of that, which is why they are there.

If I were starting again I would have flows return a result object and let tests
assert on it. The current shape is a reasonable trade that I would not defend as
the right one.

---

## 9. Evidence

Every run produces, under one folder:

- **Allure results**, with feature, story, severity and per-step breakdowns
- **A Playwright trace per test**, which is the important one
- **Screenshots** on failure, named after the action that failed
- **Video** of every context
- **Logs**, one file per run

The trace is what makes a failure diagnosable rather than merely reported.
`playwright show-trace artifacts/<run-id>/traces/<test>.zip` gives you a
timeline with DOM snapshots at every step. You can hover over the moment before
the click and see what the page actually looked like, which usually answers the
question in about ten seconds without reproducing anything.

Tracing is on for every test, not just failures, because the run that fails once
in twenty is exactly the one you cannot reproduce on demand.

---

## 10. Running in parallel, and the bug it caused

`pytest -n 2` gives two workers, and roughly halves a two-minute suite.

xdist workers are **separate processes**. Not threads. Each one imports the whole
framework independently, which means each one builds its own singletons.

`ArtifactManager.__init__` used to be:

```python
self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
```

Two processes starting a second apart get two different ids, so one run wrote
into two folders: `artifacts/20260904_100742/` and `artifacts/20260904_100743/`.
Each held roughly half the results.

CI then published whichever it found, which was sometimes the one with almost
nothing in it. **A green Allure report over a half-empty folder is worse than a
red one**, because a red report gets investigated and a green one does not. Six
tests pass, six are missing, and the report says six passed.

The fix:

```python
def _generate_execution_Id(self):
    # xdist workers are separate processes. Without a shared id each one stamps
    # its own timestamp and the run gets split across two artifact folders, one
    # of which ends up empty.
    execution_id = os.environ.get("TEST_EXECUTION_ID")
    if not execution_id:
        execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.environ["TEST_EXECUTION_ID"] = execution_id
    return execution_id
```

The controller generates it and puts it in the environment; xdist workers inherit
the environment, so every one of them resolves the same id. CI sets it explicitly
to `run-<run_id>-<run_attempt>`, which is better still because it ties the folder
to the CI run that produced it.

You can watch it work:

```bash
$ pytest -p no:playwright -m ui -n 2
$ python3 -c "
import json, glob, collections
c = collections.Counter()
for f in glob.glob('artifacts/<latest>/allure-results/*-result.json'):
    for l in json.load(open(f))['labels']:
        if l['name'] == 'thread': c[l['value']] += 1
print(c)"
Counter({'33247-MainThread': 8, '33250-MainThread': 5})
```

Two worker processes, thirteen results, one folder.

**The general lesson**, and the reason this is the story I tell about the
framework: with parallelism, anything derived independently in each process will
diverge. Timestamps, temp directories, sequence numbers, "unique" ids. It will
usually work, because the processes usually start in the same second, and it will
fail on the day the runner is busy.

---

## 11. Telling flakiness apart from failure

The suite drives a public practice site. It goes down, it sits behind Cloudflare,
and under parallel load it occasionally answers a checkout click with neither the
next page nor an error, because nothing is coming. None of that is a defect in
the code under test, and all of it will fail a build.

Three mechanisms, each aimed at a different thing.

**A reachability probe at collection.** `pytest_collection_modifyitems` fetches
one endpoint and checks the body starts with `{` or `[`:

```python
reachable, detail = _site_serves_us(framework_config.api_base_url + "/productsList")
```

If the site is down or serving a Cloudflare challenge, the tests that need it are
**skipped with the reason**, rather than failing as though the framework were
broken. Skipped-with-a-reason and failed are different signals and should look
different.

**Retries on UI tests only.**

```python
for item in items:
    if "ui" in item.keywords:
        item.add_marker(pytest.mark.flaky(reruns=2, reruns_delay=3))
```

UI tests get two. API tests get none, because an API is deterministic and
retrying one would hide a real intermittent bug. A genuine regression fails all
three attempts anyway, so this covers flakiness in the target rather than in this
code. Reruns are reported in the run summary so they stay visible: a test that
only passes on its third attempt is information, not something to hide.

**A guard on the retries themselves.** `pytest.mark.flaky` is inert without
`pytest-rerunfailures` installed. The marker still applies, nothing errors, and
the retries silently stop happening. The first symptom is a red build that passes
when you run it again by hand, which is the worst possible way to find out.

I found this the hard way on an environment missing the plugin: two UI tests
failed under `-n 2`, both passed serially, and the reruns that should have
absorbed it never fired. So collection now warns when the plugin is absent:

```python
if not config.pluginmanager.hasplugin("rerunfailures"):
    config.issue_config_time_warning(...)
```

Which is the same principle as `FileReport.error` in the reviewer and the saved
answer labels on the portfolio: **a safety net that has silently stopped working
must say so.**

---

## 12. Configuration

`config/default.env` holds the common settings, `qa.env` / `uat.env` /
`prod.env` hold only what differs, and real environment variables win over both
so CI can override without editing files.

| | |
|---|---|
| `BASE_URL` | the UI under test |
| `API_BASE_URL` | automationexercise's API |
| `DUMMYJSON_API_BASE_URL` | the second API |
| `BROWSER` | chromium, firefox or webkit |
| `HEADLESS` | true in CI |
| `DEFAULT_TIMEOUT` | every action and navigation |
| `EXPECT_TIMEOUT` | `expect()` only, set separately |

```bash
pytest --environment uat --browser firefox
```

`_validate_configuration` rejects an unknown environment or browser at startup
rather than letting it fail as a confusing error twenty seconds in.

`uat` and `prod` point at the same URLs as `qa`, because the practice site has
one deployment. They differ in timeouts and headless mode. That is honest rather
than impressive, and the alternative was inventing environments that do not
exist.

---

## 13. CI

`.github/workflows/ci.yml`, on push and pull request, in Docker.

Docker rather than installing Playwright on the runner, because the browser
version, the system libraries and the Python version are then the same
everywhere, and "works on my machine" stops being a category of failure. Buildx
layer caching keeps it from being slow.

```yaml
TEST_EXECUTION_ID: run-${{ github.run_id }}-${{ github.run_attempt }}
```

Set at the job level and passed into the container, so the artifact folder is
named after the CI run that produced it.
[Section 10](#10-running-in-parallel-and-the-bug-it-caused) is why.

The steps that matter:

**Allure history is restored before generating.** Without it, every report shows
a single run and the trend graph is one bar. The workflow copies `history/` out
of the previously published report into the new results, which is what makes the
trend accumulate across runs.

**`executor.json` is written.** That is what makes the report link back to the CI
run that produced it, so a report is traceable to a commit rather than floating
free.

**The report is published per pull request**, to `pr-<number>/`, so a PR run does
not overwrite the published main report.

**The build fails at the end, not in the middle.** The test step does not abort
the job, so the report still gets generated and published even when tests fail,
and a separate final step sets the exit code. The one run you most want to look
at is the one that failed, and that is exactly the one that would otherwise
produce no artifact.

---

## 14. Running it yourself

```bash
git clone https://github.com/Priya123z/AutomationExercise-Playwright-Python-Framework.git
cd AutomationExercise-Playwright-Python-Framework

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest                       # all 30
pytest -m api                # 17, no browser needed, ~11s
pytest -m ui -n 2            # 13 in parallel, ~90s
pytest -m smoke              # the critical path
```

Python 3.11 or newer, because `api/api_client.py` uses `enum.StrEnum`.

Or in Docker, which is what CI does:

```bash
docker build -t ae-framework .
docker run --rm ae-framework pytest -n 2
```

Reading a failure:

```bash
playwright show-trace artifacts/<run-id>/traces/<test_name>.zip
```

If you only look at one thing to understand the framework, run
`pytest -m ui -n 2` and then look at `artifacts/`. One folder, two workers,
everything in it.

---

## 15. Bugs worth knowing about

Every one of these shipped, and each left a comment in the code.

**The run split across two artifact folders.** The headline one.
[Section 10](#10-running-in-parallel-and-the-bug-it-caused).

**`DEFAULT_TIMEOUT` was never applied.** Read, validated, tuned per environment,
displayed in the report, never passed to Playwright.
[Section 6](#6-the-fixtures).

**Two screenshots per failure.** Actions nest, so one failing click unwound
through the handler twice and the second screenshot was one frame later and named
after the wrong operation. Fixed by tagging the exception.
[Section 3](#3-one-test-all-the-way-down).

**`requires-python` said 3.10 while the code needs 3.11.** `enum.StrEnum` is
3.11+. `pip install` succeeded and the first import failed, which is the worst
place to find out.

**`uv.lock` predated `pytest-rerunfailures`.** `uv sync` produced an environment
where the UI retries silently did not happen, which is the same class of bug as
the warning added in [section 11](#11-telling-flakiness-apart-from-failure) and
is what prompted it.

**Schema paths depended on the working directory.** `SchemaValidator` resolved
relative paths against the process's cwd, so running pytest from anywhere but the
repository root failed to find schemas. It now resolves against `schemas/`
explicitly.

The pattern, again: not one of these threw a clear exception at the point of the
mistake. Every one produced plausible behaviour that was wrong, and most of them
made a report *more* confident rather than less.

---

## 16. What is still wrong with it

Named honestly, and `readme.md` carries the same list.

**`config/credentials.json` holds a plaintext password.** It is read at runtime,
so it cannot simply be deleted the way the other committed junk could. It is an
account on a public practice site, not anything real, but the right shape is an
environment variable with this file as the example.

**Four things were tracked despite being in `.gitignore`** and are now untracked:
browser session state, ten stale failure screenshots, `.idea/`, and a 30 MB
Allure tarball referenced by nothing. **They are all still in git history**, and
getting them out needs a rewrite and a force push, which is a decision rather
than a cleanup.

**The API flows assert.** [Section 8](#8-three-tier-validation) argues both
sides. I would do it differently now.

**`uat` and `prod` are `qa` with different timeouts.** There is one deployment of
the practice site.

**`test_data/users/users.json` is read by nothing** now that the login tests
create their own accounts. Kept as an example of the reader layer, which the
payment data does exercise.

**Coverage is breadth, not depth.** Thirty tests over registration, login,
search, cart, checkout and payment is a demonstration of a structure, not a
regression suite for a real product.

---

## 17. FAQ

**Why Playwright rather than Selenium?**
Auto-waiting removes most explicit sleeps, the trace viewer is a genuinely better
debugging story than a screenshot, and one `APIRequestContext` covers UI and API
so both share a stack. I have shipped plenty of Selenium; this is better.

**Why page objects when Playwright's locators are already readable?**
Because the readability is at the call site, not at the maintenance site. Fifteen
tests each writing `page.locator("[data-qa='login-email']")` is fifteen edits when
that attribute changes. The point of the layer is the edit, not the reading.

**Why do page methods return other page objects?**
So a test reads as a journey without naming a navigation, and so the type at each
step says where you are. It is the thing that makes the six-line login test
possible.

**Why `-n 2` and not more?**
Two workers is what a free GitHub runner has cores for, and the target is a
public practice site that rate limits. More workers would trade a red build for a
slightly faster one.

**Why retry UI tests but not API tests?**
An API is deterministic; retrying one would hide a real intermittent bug. A
browser against a public site under parallel load is not. The retries are
reported so a test that only passes on the third attempt stays visible.

**Is retrying not just hiding failures?**
It would be, if it were unconditional and silent. It is neither: UI only, two
attempts, counted in the summary, and a genuine regression fails all three. And
the suite now warns when the retry plugin is missing, which is the failure mode
that actually worries me.

**Why Docker in CI?**
So the browser version, the system libraries and the Python version are identical
everywhere. It also means `docker run` reproduces a CI failure exactly.

**Why does the build publish a report even when tests fail?**
Because the failing run is the one you want to look at. The job still fails, at
the last step.

**Why is `TEST_EXECUTION_ID` an environment variable rather than a file?**
Because xdist workers inherit the environment and are separate processes. A file
would need locking; the environment is already shared, already ordered, and
already inherited.

**What would you change first?**
Make the API flows return results instead of asserting, then move those
assertions into the tests where the layering says they belong.
