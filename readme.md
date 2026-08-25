# Automation Exercise - Playwright Python Framework

A scalable UI and API automation framework built with **Playwright and
Python**.

What started as a collection of automation scripts gradually evolved
into a maintainable framework as the project grew in size and
complexity. This repository focuses on scalability, reusability, clean
architecture, reliable test execution, and useful diagnostics rather
than simply automating test cases.

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

1.  Checkout of the repository
2.  Python environment setup
3.  Dependency installation
4.  Playwright browser installation
5.  Parallel test execution
6.  Allure result generation
7.  Allure HTML report generation
8.  Upload of Allure results as an artifact
9.  Upload of the generated Allure HTML report as an artifact

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
```

or:

``` bash
pytest --browser=firefox
pytest --browser=webkit
```

------------------------------------------------------------------------

# Allure Reports

Generate Allure results while running the suite:

``` bash
pytest -q --alluredir=allure-results
```

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

## Next

-   [ ] Docker integration
-   [ ] Database testing
-   [ ] Performance testing
-   [ ] Security testing
-   [ ] AI-assisted test generation and maintenance

------------------------------------------------------------------------

# Contributing

This is primarily a personal/portfolio project, but suggestions and
issues are welcome.

If you identify an improvement in architecture, maintainability,
reliability, or test coverage, feel free to open an issue or pull
request.

------------------------------------------------------------------------

# Contact

**Priya**\
Senior Software Development Engineer in Test (SDET)

Automation \| Playwright \| Python \| API Testing

-   LinkedIn: https://www.linkedin.com/in/priya-bhagoriya/
-   GitHub: https://github.com/Priya123z

------------------------------------------------------------------------

# License

MIT