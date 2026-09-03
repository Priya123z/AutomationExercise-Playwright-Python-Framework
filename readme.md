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

------------------------------------------------------------------------

## Why this project exists

Writing automated tests is easy. Keeping a growing automation suite
maintainable is not.

As the suite grew, the framework needed better separation of
responsibilities, reusable components, centralized configuration,
reliable diagnostics, API abstraction, and CI/CD support.

The goal is to build automation that is:

-   Maintainable
-   Reusable
-   Scalable
-   Debuggable
-   CI/CD ready

------------------------------------------------------------------------

## Tech Stack

-   **Python** - Core programming language
-   **Playwright** - UI and API automation
-   **Pytest** - Test runner, fixtures, parameterization, and test
    organization
-   **pytest-xdist** - Parallel test execution
-   **Allure** - Interactive test reporting
-   **JSON Schema** - API contract validation
-   **Faker** - Dynamic test data generation
-   **Loguru** - Centralized logging
-   **OpenPyXL** - Excel test-data support
-   **python-dotenv** - Environment configuration
-   **Git / GitHub** - Version control
-   **GitHub Actions** - CI/CD execution

------------------------------------------------------------------------

## Architecture

The framework separates test scenarios from implementation details.

``` text
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

                  COMMON FRAMEWORK LAYERS
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
        TEST DATA      CONFIGURATION     UTILITIES
        FACTORIES       MANAGEMENT       & LOGGING
             |               |               |
             +---------------+---------------+
                             v
                       VALIDATION
                             |
                  +----------+----------+
                  |                     |
                  v                     v
             JSON Schema           Business
             Validation            Validation
```

------------------------------------------------------------------------

## Project Structure

``` text
AutomationExercise-Playwright-Python-Framework/
|
+-- api/
|   +-- api_client.py
|   +-- auth_api.py
|   +-- product_api.py
|   +-- endpoints.py
|
+-- config/
|   +-- qa.env
|   +-- uat.env
|   +-- prod.env
|
+-- flows/
|   +-- API_Flow/
|       +-- auth_flow.py
|       +-- auth_negative_flow.py
|       +-- product_flow.py
|
+-- models/
|   +-- ...
|
+-- pages/
|   +-- ...
|
+-- schemas/
|   +-- ...
|
+-- tests/
|   +-- UI/
|   +-- api/
|
+-- test_data/
|   +-- ...
|
+-- utils/
|   +-- factories/
|   +-- readers/
|   +-- authentication/
|   +-- artifact_manager.py
|   +-- config_manager.py
|   +-- logger.py
|   +-- schema_validator.py
|   +-- test_data.py
|   +-- ...
|
+-- artifacts/
|   +-- ...
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- conftest.py
+-- pytest.ini
+-- requirements.txt
+-- .gitignore
+-- README.md
```

> Generated reports, logs, screenshots, traces, videos, Allure results,
> environment files, and virtual environments should not be committed to
> Git.

------------------------------------------------------------------------

# Features

## UI Automation

-   Playwright with Python
-   Page Object Model
-   Reusable page components
-   Browser Factory
-   Chromium / Firefox / WebKit support
-   Pytest fixtures
-   Dynamic test data
-   Business-oriented UI flows
-   Automatic screenshots on failure
-   Tracing and video capture for diagnostics

## API Automation

The API layer follows a layered architecture:

``` text
Test
  |
  v
Flow
  |
  v
API
  |
  v
API Client
  |
  v
Endpoint
```

The framework currently covers:

-   REST API testing
-   CRUD operations
-   Request/response models
-   Centralized API client
-   Endpoint management
-   API chaining
-   Positive and negative scenarios
-   HTTP validation
-   Business validation
-   JSON Schema contract validation
-   API response attachments in Allure

------------------------------------------------------------------------

## API Chaining

The framework supports multi-step API workflows.

Example:

``` text
Create User
     |
     v
Login User
     |
     v
Delete User
```

Dynamically generated test data can be passed from one operation to the
next, allowing dependent API operations to be validated as an end-to-end
workflow rather than isolated requests.

------------------------------------------------------------------------

# API Validation Strategy

API responses are validated at multiple levels.

### 1. HTTP Validation

Validates the actual HTTP response status.

``` python
assert response.status == 200
```

### 2. Business Validation

Validates application-specific response values.

``` python
assert login_body.responseCode == 200
assert login_body.message == "User exists!"
```

### 3. Contract Validation

Validates the response structure against a JSON Schema.

``` python
SchemaValidator.validate_response(
    response,
    "schemas/auth/login_user_schema.json"
)
```

This helps detect breaking API contract changes even when the HTTP
status code is successful.

------------------------------------------------------------------------

# Test Data Management

The framework uses reusable test-data factories instead of hard-coded
data.

``` python
user = UserFactory.create()
```

Dynamic data generation is supported through **Faker**.

Structured test data is also supported through:

-   CSV
-   Excel
-   JSON
-   Pytest parameterization

This keeps test data separate from test logic and makes scenarios easier
to extend.

------------------------------------------------------------------------

# Configuration Management

Environment-specific configuration is separated from test logic.

Current configuration includes values such as:

-   `BASE_URL`
-   `API_BASE_URL`
-   `DUMMYJSON_API_BASE_URL`
-   `BROWSER`
-   `HEADLESS`
-   `DEFAULT_TIMEOUT`
-   `EXPECT_TIMEOUT`

Example:

``` text
config/qa.env

BASE_URL=https://automationexercise.com/
API_BASE_URL=https://automationexercise.com/api
BROWSER=chromium
HEADLESS=True
DEFAULT_TIMEOUT=10000
EXPECT_TIMEOUT=20000
```

Environment files containing sensitive values should remain local and
must not be committed to Git.

In CI, environment-specific values are supplied through GitHub Actions
configuration rather than hard-coding secrets into the workflow.

------------------------------------------------------------------------

# Logging & Diagnostics

Centralized logging is implemented using **Loguru**.

Logs help answer:

-   What action was being performed?
-   Which test was executing?
-   Which API request was sent?
-   Where did execution fail?

For UI failures, screenshots are captured automatically using a Pytest
test-result hook.

Playwright tracing and video recording are also enabled through the test
fixtures to make failures easier to investigate.

Execution artifacts are organized by execution ID:

``` text
artifacts/
+-- <execution_id>/
    +-- logs/
    +-- screenshots/
    +-- reports/
    +-- videos/
    +-- traces/
    +-- allure-results/
```

------------------------------------------------------------------------

# Allure Reporting

The framework uses **Allure** for interactive test reporting.

Current capabilities include:

-   Features
-   Stories
-   Test titles
-   Test descriptions
-   Severity
-   Execution steps
-   API response attachments
-   Allure results generated during CI execution
-   HTML Allure report generated in CI
-   Allure results and report uploaded as GitHub Actions artifacts

Example:

``` python
@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Register a new user successfully")
@allure.severity(allure.severity_level.CRITICAL)
```

Execution steps can be represented using:

``` python
with allure.step("Register user"):
    response, register_body = self.auth_api.register(user)
```

API responses can also be attached to the report:

``` python
allure.attach(
    response.text(),
    name="Register API Response",
    attachment_type=allure.attachment_type.JSON
)
```

------------------------------------------------------------------------

# GitHub Actions CI/CD

The framework is integrated with **GitHub Actions**.

The CI workflow currently performs:

1.  Checkout
2.  Docker image build, with layer caching between runs
3.  Test execution inside the container, two parallel workers
4.  Result summary written to the job summary
5.  Allure history restored from the previous publish, so trends accumulate
6.  Allure report generation
7.  Publish to GitHub Pages — `main` to the site root, a pull request to `pr-<number>/`
8.  Pull request comment with the counts and a link to that report
9.  Artifact upload of the whole run for 14 days

Everything after the test step runs even when tests fail, so a red run still
publishes a report explaining why. The job then fails on the test outcome.

The container runs as the host uid, so nothing on the mounted volume comes back
owned by root. The results folder is named from `TEST_EXECUTION_ID`, set by the
workflow, rather than searched for afterwards — see the note under Artifacts.

The workflow runs for pushes and pull requests targeting the configured
branches.

The test suite has been validated locally and in GitHub Actions with
**two parallel workers** using `pytest-xdist`.

Example local execution:

``` bash
pytest -n 2 -q
```

CI execution:

``` bash
pytest -n 2 -q --alluredir=allure-results
```

> Because the UI tests use a public practice application, occasional
> external-site issues such as transient availability or Cloudflare
> responses can occur. These are investigated separately from
> framework-level failures using screenshots, traces, logs, and Allure
> artifacts.

------------------------------------------------------------------------

# CI Artifacts

The workflow preserves test diagnostics even when tests fail.

Important artifacts include:

``` text
allure-results/
allure-report/
```

These are uploaded to the GitHub Actions run so that test results can be
inspected after execution.

This makes CI failures easier to diagnose without reproducing the run
locally.

------------------------------------------------------------------------

# Getting Started

## Prerequisites

-   Python 3.10+
-   pip
-   Git
-   Playwright

## Clone the repository

``` bash
git clone https://github.com/Priya123z/AutomationExercise-Playwright-Python-Framework.git

cd AutomationExercise-Playwright-Python-Framework
```

## Create a virtual environment

``` bash
python -m venv .venv
```

Activate it on Linux/macOS:

``` bash
source .venv/bin/activate
```

## Install dependencies

``` bash
pip install -r requirements.txt
```

Install Playwright browsers:

``` bash
playwright install
```

------------------------------------------------------------------------

# Running Tests

## Run the complete suite

``` bash
pytest -q
```

## Run UI tests

``` bash
pytest tests/UI -q
```

## Run API tests

``` bash
pytest tests/api -q
```

## Run a specific test file

``` bash
pytest tests/UI/test_login.py -q
```

## Run in parallel

``` bash
pytest -n 2 -q
```

## Run a specific browser

``` bash
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

Or by environment, which is what CI uses:

``` bash
BROWSER=firefox pytest -q
pytest --environment=uat        # qa, uat or prod
```

Both options were previously accepted and then ignored, because the config
singleton was built at import time with the environment hardcoded. They take
effect now, and an unknown value is rejected with a usage error rather than
silently falling back.

The Docker image installs Chromium only. Run the other two locally.

------------------------------------------------------------------------

# Allure Reports

Generate Allure results while running the suite:

``` bash
pytest -q
```

`--alluredir` is not needed: `pytest_configure` points Allure at this run's
artifacts folder.

Generate and open the interactive report locally:

``` bash
allure serve allure-results
```

For CI executions, the generated Allure results and HTML report are
available through the GitHub Actions workflow artifacts.

------------------------------------------------------------------------

# Design Principles

### Scalability

The framework structure makes it possible to add new tests without
unnecessarily modifying existing components.

### Maintainability

Responsibilities are separated between tests, flows, pages, APIs,
utilities, configuration, and validation.

### Reusability

Common functionality such as browser management, API communication, test
data generation, logging, and validation is centralized.

### Debuggability

A failure should provide enough information to understand what happened
without immediately reproducing it.

This is supported through:

-   Logs
-   Screenshots
-   Videos
-   Traces
-   Allure reports
-   API response attachments

### Separation of Concerns

Tests describe **what** should be validated.

Flows describe **business workflows**.

Page objects describe **UI interactions**.

API classes describe **API operations**.

The API client handles **HTTP communication**.

------------------------------------------------------------------------

# Roadmap

## Completed

-   [x] Framework setup
-   [x] Playwright UI automation
-   [x] Page Object Model
-   [x] Cross-browser support
-   [x] Browser Factory
-   [x] Configuration management
-   [x] Centralized logging
-   [x] Failure screenshots
-   [x] Playwright traces and video capture
-   [x] API automation
-   [x] API CRUD operations
-   [x] API chaining
-   [x] Test data factories
-   [x] CSV / Excel / JSON test data support
-   [x] JSON Schema validation
-   [x] HTTP / Business / Contract validation
-   [x] Allure reporting
-   [x] Allure steps
-   [x] API response attachments
-   [x] Execution artifact management
-   [x] GitHub Actions CI/CD
-   [x] Allure reporting in CI
-   [x] CI artifact management
-   [x] Environment variables in CI
-   [x] Parallel execution with pytest-xdist

-   [x] Docker execution in CI
-   [x] Published Allure report with trend history
-   [x] Pull request result comments
-   [x] Marker taxonomy with `--strict-markers`

## Next

-   [ ] Database testing
-   [ ] Performance testing
-   [ ] Security testing
-   [ ] AI-assisted test generation and maintenance

------------------------------------------------------------------------

# Selecting tests

``` bash
pytest -m smoke        # 8 of 30, the critical path
pytest -m api          # 17
pytest -m ui           # 13
pytest -m auth         # 13
pytest -m "ui and cart"
```

Markers are declared in `pytest.ini` and enforced with `--strict-markers`, so a
typo in a decorator fails collection instead of silently marking nothing.

Note that `--strict-markers` validates decorators, not `-m` expressions. A typo
in `-m` deselects everything and exits cleanly — check the collected count.

------------------------------------------------------------------------

# Artifacts, and one bug worth reading about

Each run writes to `artifacts/<execution id>/`:

```
artifacts/<id>/
+-- allure-results/     raw results, plus environment.properties
+-- allure-report/      generated report
+-- reports/            pytest-html
+-- logs/               framework.log
+-- screenshots/        on failure
+-- traces/             one Playwright trace per test
+-- videos/
+-- auth/               storage state, rebuilt per run
+-- junit.xml
```

The execution id used to be a per-second timestamp taken when
`ArtifactManager` was first imported. Under `pytest -n`, every xdist worker is a
separate process, so two workers starting either side of a second boundary each
created their own folder — and one of them ended up empty. CI selected a folder
with `find -print -quit`, which returns directory order rather than the one with
results in it, so the published report could contain half the run or none of it.
It reproduced in two of three runs.

The id now comes from `TEST_EXECUTION_ID` in the environment, which every worker
inherits, and CI sets it up front so it knows the path without searching.

Storage state also lives here rather than in the repository. It is created once
per run and reused, where previously it was deleted and recreated for every test
that asked for it, so the optimisation bought nothing.

------------------------------------------------------------------------

# Test accounts

The UI login tests used to read six accounts out of `test_data/users/users.json`
and expect them to exist on the site, running the same login flow six times with
different credentials. Those are accounts on a shared public practice app, so
other people delete them and the site resets, and the tests failed for reasons
that had nothing to do with this code.

A `registered_user` fixture now creates the account over the API, hands it to the
test, and deletes it afterwards. One API call, always works, and the site is left
as it was found. Data-driven parametrisation is still used where the data
actually changes behaviour — payment details, product ids — rather than to run
one code path repeatedly.

That is why the suite is 30 tests rather than the 45 it collected before. The
eighteen removed cases were the same three flows repeated across six accounts,
which added no distinct assertions.

## Retries

UI tests get two retries, applied in `pytest_collection_modifyitems`. Under
parallel load the practice site occasionally answers a checkout click with
neither the address page nor the register prompt, and no amount of waiting fixes
that because nothing is coming. API tests get none, and a genuine regression
fails every attempt, so this covers flakiness in the target rather than in this
code. Reruns are reported in the run summary so they stay visible.

------------------------------------------------------------------------

# Known issues

Being honest about what is still wrong here:

-   `config/credentials.json` holds a plaintext password, and
    `utils/auth/qa/*.json` holds committed browser session state. Both are in
    `.gitignore`, but they were committed before that rule existed, so they are
    still tracked and still in history. They are credentials for a public
    practice site, not a real system, but they should be purged and rotated.
-   `allure-2.45.0.tgz`, 30 MB, is committed and used by nothing. CI installs the
    Allure CLI from npm. It is excluded from the Docker build context but remains
    in git history.
-   `.idea/` and `screenshots/` are tracked for the same reason, and `.idea/`
    leaks a local path.
-   Removing all of the above needs a history rewrite and a force push, which is
    a deliberate decision rather than a cleanup.
-   `uat` and `prod` point at the same URLs as `qa`, because the practice site has
    only one deployment. They differ in timeouts and headless mode only.
-   The suite drives a public site. Cloudflare responses and outages will still
    fail runs for reasons unrelated to this code; retries cover the transient
    cases, not an outage.
-   `test_data/users/users.json` is still committed and still read by nothing
    now that the login tests create their own accounts. It is kept as an example
    of the reader layer, which does get exercised by the payment data.

------------------------------------------------------------------------

# Contributing

This is primarily a personal/portfolio project, but suggestions and
issues are welcome.

If you identify an improvement in architecture, maintainability,
reliability, or test coverage, feel free to open an issue or pull
request.

------------------------------------------------------------------------

# Contact

**Priya Bhagoriya**\
SDET / AI Test Engineer

-   Portfolio: https://priya123z.github.io

-   LinkedIn: https://www.linkedin.com/in/priya-bhagoriya/
-   GitHub: https://github.com/Priya123z

------------------------------------------------------------------------

# License

MIT