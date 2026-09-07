# AutomationExercise Playwright Python Framework

UI and API test automation for [automationexercise.com](https://automationexercise.com),
built with Playwright and Pytest, running in Docker on GitHub Actions.

### [→ Open the live report](https://priya123z.github.io/AutomationExercise-Playwright-Python-Framework/)

Published by CI on every commit: 30 tests, per-step detail, trend history across
runs, and screenshots and traces on the failures.

[![Tests](https://github.com/Priya123z/AutomationExercise-Playwright-Python-Framework/actions/workflows/ci.yml/badge.svg)](https://github.com/Priya123z/AutomationExercise-Playwright-Python-Framework/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-1.61-45ba4b)
![Tests](https://img.shields.io/badge/tests-30-brightgreen)

Every pull request gets a comment with the pass/fail counts and a link to its own
copy of the report, published under `pr-<number>/`.

## Why this exists

Writing automated tests is easy. Keeping a growing suite maintainable is not.
The goal here is a layout that does not need rewriting at fifty tests: a test
reads as intent and never touches a selector, a URL or a wait, and everything
underneath it (config, browsers, auth, artifacts, reporting) sits behind
fixtures.

It tests a public practice site, so the coverage is not the interesting part.
The framework around the tests is.

## If you have five minutes

**Open the [live report](https://priya123z.github.io/AutomationExercise-Playwright-Python-Framework/) first.**
It is the output; everything below is how it gets made.

Then read three files, in this order:

| File | Why this one |
|---|---|
| [`tests/UI/test_login.py`](tests/UI/test_login.py) | What a test looks like here: nineteen lines, no selectors, no waits, no URLs. Just intent and one assertion. If this reads clearly, the layering is doing its job. |
| [`flows/API_Flow/auth_flow.py`](flows/API_Flow/auth_flow.py) | The layer between a test and an API client, and where the three-tier validation lives: HTTP status, then the business response, then the JSON Schema. A 200 carrying the wrong body fails here. |
| [`conftest.py`](conftest.py) | Every fixture and hook, including the parts that are not obvious: accounts created over the API rather than read from committed data, a preflight that skips with a reason when the site blocks CI, and reruns applied to UI tests only. |

Then, if you want the interesting part: [the execution-id
bug](#artifacts-and-one-bug-worth-reading-about), a genuine parallel-execution
defect that could publish half a test run as though it were the whole thing.

## Architecture

One direction only. A test never reaches past the layer below it.

```
                         TEST CASES
                             |
                             v
                      BUSINESS FLOWS
                             |
              +--------------+--------------+
              |                             |
              v                             v
         PAGE OBJECTS                    API LAYER
              |                             |
              v                             v
        PLAYWRIGHT UI                   API CLIENT
                                            |
                                            v
                                        ENDPOINTS
```

Underneath, shared by both sides: configuration, test-data factories, logging,
artifact management, and schema validation.

| Layer | Holds | Never holds |
|---|---|---|
| `tests/` | intent, and the assertion | selectors, URLs, waits, payloads |
| `flows/` | a business workflow, and its validation | element lookups, HTTP calls |
| `pages/`, `components/` | selectors and page transitions | assertions about business rules |
| `api/` | endpoints, payload shaping, retries | test data, assertions |
| `utils/` | config, factories, logging, artifacts, schemas | anything about this site |

## Project structure

```
api/            api_client (retries, non-JSON guard), auth, product, endpoints
components/     navbar, cart modal, checkout modal
config/         default.env plus qa/uat/prod overrides, allure categories
flows/          API_Flow, UI_Flow: the business workflows tests call
models/         automationexercise.py, dummyjson.py: request and record shapes
pages/          one page object per page, signup_login_page/ for the flow
schemas/        JSON Schema contracts, applied to API responses
test_data/      payment and product data, read as JSON
tests/          UI/ and api/, 30 tests
utils/          config, artifacts, auth, logging, factories, schema validation
conftest.py     every fixture and hook
Dockerfile      python:3.12-slim plus chromium, what CI runs
pytest.ini      markers, enforced with --strict-markers
```

Reports, logs, screenshots, traces, videos and Allure results are written under
`artifacts/<run id>/` and are not committed.

## Getting started

```bash
git clone https://github.com/Priya123z/AutomationExercise-Playwright-Python-Framework.git
cd AutomationExercise-Playwright-Python-Framework

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest -q
```

Nothing to configure. There are no secrets and no accounts to create: the tests
that need one register it over the API and delete it afterwards.

Python 3.10 or newer. CI and the Docker image run 3.12.

## Running tests

```bash
pytest -q                       # all 30
pytest -n 2 -q                  # two workers, which is what CI uses
pytest tests/UI -q              # 13 browser tests
pytest tests/api -q             # 17 API tests
pytest tests/UI/test_login.py -q

BROWSER=firefox pytest -q       # chromium, firefox or webkit
HEADLESS=False pytest -q
pytest --environment=uat        # qa, uat or prod
```

`BROWSER` is an environment variable rather than a `--browser` flag on purpose:
`pytest-playwright` registers an option by that name, and anyone with that
plugin installed used to get an argparse conflict before collection started,
with nothing explaining why.

The Docker image installs Chromium only. Run the other two locally.

### Selecting tests

```bash
pytest -m smoke        # 8 of 30, the critical path
pytest -m api          # 17
pytest -m ui           # 13
pytest -m auth         # 13
pytest -m products     # 10
pytest -m negative     # 8
pytest -m "ui and cart"
```

Markers are declared in `pytest.ini` and enforced with `--strict-markers`, so a
typo in a decorator fails collection instead of silently marking nothing. Note
that `--strict-markers` validates decorators, not `-m` expressions: a typo in
`-m` deselects everything and exits cleanly, so check the collected count.

## In Docker

```bash
docker build -t automationexercise-tests .
mkdir -p artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -e TEST_EXECUTION_ID=local \
  -e HEADLESS=true -e BROWSER=chromium \
  -v "$PWD/artifacts:/app/artifacts" \
  automationexercise-tests
```

The container runs as the host uid, so nothing on the mounted volume comes back
owned by root. The image is built as uid 1000 but GitHub runners are 1001, and
that mismatch is a mistake worth not repeating: browsers are installed to
`/ms-playwright` and made world-readable, and `HOME` is `/tmp`, so an arbitrary
`--user` can still find them and still write pytest's scratch files.

## API validation, in three tiers

A 200 is not a pass.

```python
assert response.status == 200                       # HTTP
assert login_body["responseCode"] == 200            # business
SchemaValidator.validate_response(                  # contract
    response, "auth/login_user_schema.json"
)
```

The schemas live in `schemas/` as their own files and all set
`additionalProperties: false`, so a field being added, removed or retyped fails
the build even when the status code is fine. That is the break a status-code
assertion cannot see.

## Reporting

Allure, generated in CI and published to Pages. Each run carries features,
stories, titles, severities, per-step detail, and the API response attached to
the step that made the call:

```python
@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Register a new user successfully")
@allure.severity(allure.severity_level.CRITICAL)
```

Locally, `pytest -q` writes Allure results into this run's artifacts folder
without needing `--alluredir`, and `allure serve artifacts/<run id>/allure-results`
opens the report.

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml), on every push and pull
request:

1. build the image, with layer caching between runs
2. run the suite in the container, two workers
3. write the pass/fail summary into the job summary
4. restore the previous Allure history, so trends accumulate
5. generate the report and publish it: `main` to the site root, a pull request
   to `pr-<number>/`
6. comment the counts on the pull request, editing one comment rather than
   appending
7. upload the whole run as an artifact for 14 days

Everything after the test step runs even when tests fail, so a red run still
publishes a report explaining why. The job then fails on the test outcome.

## Artifacts, and one bug worth reading about

Each run writes to `artifacts/<execution id>/`:

```
allure-results/     raw results, plus environment.properties and categories.json
allure-report/      generated report
reports/            pytest-html
logs/               framework.log
screenshots/        on failure
traces/             one Playwright trace per test
videos/
auth/               storage state, rebuilt per run
junit.xml
```

The execution id used to be a per-second timestamp taken when `ArtifactManager`
was first imported. Under `pytest -n`, every xdist worker is a separate process,
so two workers starting either side of a second boundary each created their own
folder, and one of them ended up empty. CI selected a folder with
`find -print -quit`, which returns directory order rather than the one with
results in it, so the published report could contain half the run or none of it.
It reproduced in two of three runs.

The id now comes from `TEST_EXECUTION_ID` in the environment, which every worker
inherits, and CI sets it up front so it knows the path without searching.

## Test accounts

The UI login tests used to read six accounts out of a committed
`test_data/users/users.json` and expect them to exist on the site. Those are
accounts on a shared public practice app, so other people delete them and the
site resets, and the tests failed for reasons that had nothing to do with this
code. Worse, the signup flow appended every account it created back into that
same committed file, so the suite grew and the working tree went dirty on every
run.

Accounts are created over the API now, handed to the test, and deleted
afterwards: `registered_user` for a test that wants its own, `standing_account`
once per run behind the authenticated fixtures. Accounts a run creates are
recorded under its artifacts folder, not in the repository.

That is why the suite is 30 tests. The cases that went were the same three flows
repeated across six accounts, which added no distinct assertions.

Data-driven parametrisation is still used where the data changes behaviour:
payment details, product ids.

## When the site will not talk to CI

automationexercise.com sits behind Cloudflare, which serves an HTML challenge to
datacenter addresses. From a GitHub runner that intermittently means every test
touching the site fails, and the failures look like defects: element not found,
`JSONDecodeError: Expecting value: line 1 column 1`. They are not defects, and
no credential or retry fixes them, because the challenge comes before the site
does.

Two things make the suite say what actually happened:

- `APIClient` checks the body starts as JSON and raises with the status and the
  first 160 characters if not, instead of letting `response.json()` fail later
  with a decode error that names nothing.
- A preflight probe runs once at collection. If the site is not answering this
  host with JSON, the tests that need it are **skipped with the reason** and the
  DummyJSON tests still run. A skipped test with an explanation is honest; a
  failed test blames code that is fine.

`APIClient` also retries 429 and 5xx with backoff, up to four attempts.
DummyJSON rate-limited a CI run and failed six tests for that reason alone. 4xx
is never retried: the negative tests assert on those, and retrying a 404 would
break them.

## Retries

UI tests get two retries, applied in `pytest_collection_modifyitems`. Under
parallel load the practice site occasionally answers a checkout click with
neither the address page nor the register prompt, and no amount of waiting fixes
that because nothing is coming. API tests get none, so a genuine regression
fails every attempt. Reruns are reported in the run summary so they stay visible.

## Known limitations

- The suite drives a public site. Cloudflare responses and outages will fail
  runs for reasons unrelated to this code; retries cover the transient cases,
  not an outage.
- `uat` and `prod` point at the same URLs as `qa`, because the practice site has
  only one deployment. They differ in timeouts and headless mode only.
- `ArtifactManager` and `ConfigManager` are singletons built at import time, so
  importing the package creates a run folder as a side effect. It is what makes
  `pytest` work with no flags, and it is not free.

## Contact

**Priya Bhagoriya**, SDET / AI Test Engineer

- Portfolio: https://priya123z.github.io
- LinkedIn: https://www.linkedin.com/in/priya-bhagoriya/
- GitHub: https://github.com/Priya123z

MIT.
