````markdown

# Automation Exercise - Playwright Python

A UI and API automation framework built with Playwright, Python and Pytest.

This project started as a collection of automation scripts for the Automation Exercise application. As the number of tests grew, I gradually started introducing proper framework components instead of keeping everything inside individual test cases.

The focus of this project is not just writing automated tests, but building something that is easier to maintain, debug and extend.

## Why this exists

Writing a few automated tests is fairly straightforward. The challenge starts when the test suite grows.

I wanted to avoid having test cases filled with browser setup, API calls, test data creation, assertions and configuration. So the framework is structured around separate responsibilities for pages, flows, APIs, test data, configuration and utilities.

The idea is simple:

**Tests should describe what is being tested, while the framework handles how it is tested.**

---

## Tech Stack

- **Python** - Core programming language
- **Playwright** - UI and API automation
- **Pytest** - Test execution and fixtures
- **Allure** - Test reporting
- **JSON Schema** - API response/contract validation
- **Faker** - Dynamic test data generation
- **Loguru** - Logging
- **OpenPyXL** - Excel test data
- **python-dotenv** - Environment configuration

---

## Project Structure

```text
AutomationExercise-Playwright-Python/
│
├── api/                # API client, API implementations and endpoints
├── config/             # Configuration and environment management
├── flows/              # Business flows
├── models/             # Request and response models
├── pages/              # Page Object Models and UI components
├── schemas/            # JSON schemas for API contract validation
├── tests/              # UI and API test cases
├── test_data/          # Test data
├── utils/              # Factories, readers, logging and utilities
│
├── artifacts/          # Execution artifacts
├── conftest.py         # Pytest fixtures and hooks
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Python dependencies
└── README.md
````

The basic flow looks like this:

```text
Test
 ↓
Flow
 ↓
 ├── Page Object → Playwright
 │
 └── API Layer → API Client → Endpoint
```

Common utilities such as configuration, logging, test data and validation are shared across the framework.

---

# UI Automation

The UI layer uses Playwright's Python sync API and follows the Page Object Model.

The goal is to keep browser interactions inside page objects instead of putting selectors and UI actions directly into tests.

A typical test therefore looks more like a business scenario:

```python
user = UserFactory.create()

home = HomePage(page)

signup_login = home.navbar.open_signup_login()
signup_login.is_loaded()

signup_page = signup_login.start_signup(user)
signup_page.is_loaded()

account_created = signup_page.create_account(user)
account_created.is_loaded()

home = account_created.continue_to_home()

assert home.user_logged_in()
```

This keeps the test readable while the actual UI implementation remains inside the page objects.

---

# API Automation

The API layer is built using Playwright's API capabilities.

Instead of making API calls directly from tests, the framework separates the API implementation into an API client and API-specific classes.

```text
Test
 ↓
Flow
 ↓
AuthAPI
 ↓
APIClient
 ↓
Endpoint
```

The current API automation includes:

* User registration
* User login
* Account deletion
* CRUD operations
* Positive and negative scenarios
* Request/response models
* API chaining

---

# API Chaining

One of the things I wanted to avoid was treating every API request as a completely isolated test.

For example, a realistic authentication workflow can be:

```text
Create User
    ↓
Login User
    ↓
Delete User
```

The framework passes the generated user through the workflow.

For example:

```python
user = self.register_and_verify_user()

user = self.register_and_verify_login(user)

user, delete_body = self.register_and_verify_delete(user)
```

This makes it possible to test dependent API operations as part of a single business flow.

---

# API Response Validation

API validation is split into three levels.

### 1. HTTP Validation

First, I validate the actual HTTP response.

```python
assert response.status == 200
```

### 2. Business Validation

Then I validate the values returned by the application.

```python
assert login_body.responseCode == 200
assert login_body.message == "User exists!"
```

### 3. Contract Validation

Finally, the response is validated against a JSON Schema.

```python
SchemaValidator.validate_response(
    response,
    "schemas/auth/login_user_schema.json"
)
```

This is useful because a `200` response by itself doesn't tell us whether the response has the structure the consumer expects.

---

# Test Data

Test data is generated through reusable factories rather than being hard-coded inside individual tests.

For example:

```python
user = UserFactory.create()
```

Faker is used to generate unique user information so that tests don't repeatedly depend on the same static data.

The framework also has support for reading test data from:

* CSV
* Excel
* JSON

---

# Configuration

Environment-specific values are kept outside the test code.

The configuration layer handles things such as:

* Base URL
* API Base URL
* Browser
* Headless execution
* Environment-specific settings

Sensitive values should not be committed to Git.

A `.env.example` file can be used to show which configuration values are required without exposing actual credentials.

---

# Logging and Failure Debugging

One of the things I wanted from the framework was better information when a test fails.

The framework uses Loguru for centralized logging.

For UI failures, screenshots are automatically captured using a Pytest test-result hook.

Execution artifacts are grouped by execution ID:

```text
artifacts/
└── <execution_id>/
    ├── logs/
    ├── screenshots/
    ├── reports/
    ├── videos/
    ├── traces/
    └── allure-results/
```

The idea is that when a test fails, I should be able to look at the logs, screenshot and report and understand what happened without immediately having to reproduce the failure locally.

---

# Allure Reporting

Allure is used for test reporting and debugging.

The framework currently uses:

* Features
* Stories
* Test titles
* Descriptions
* Severity
* Execution steps
* API response attachments

For example:

```python
@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Register a new user successfully")
@allure.severity(allure.severity_level.CRITICAL)
```

Individual operations are also grouped into readable steps:

```python
with allure.step("Register user"):
    response, register_body = self.auth_api.register(user)
```

API responses can be attached directly to the report:

```python
allure.attach(
    response.text(),
    name="Register API Response",
    attachment_type=allure.attachment_type.JSON
)
```

This makes the Allure report useful not only for seeing whether a test passed or failed, but also for understanding what happened during execution.

---

# Getting Started

## Prerequisites

* Python 3.10+
* pip
* Git

## Clone the repository

```bash
git clone https://github.com/Priya123z/AutomationExercise-Playwright-Python.git

cd AutomationExercise-Playwright-Python
```

## Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

# Running Tests

Run the complete suite:

```bash
pytest
```

Run API tests:

```bash
pytest tests/api
```

Run UI tests:

```bash
pytest tests/UI
```

Run a specific test file:

```bash
pytest tests/api/test_auth.py
```

Run against a specific browser:

```bash
pytest --browser=chromium
```

or:

```bash
pytest --browser=firefox
```

```bash
pytest --browser=webkit
```

---

# Allure Report

Run the tests with Allure results enabled:

```bash
pytest --alluredir=allure-results
```

Then open the report:

```bash
allure serve allure-results
```

The generated Allure results and other execution artifacts should not be committed to Git.

---

# Design Principles

A few principles I am trying to follow while building this framework:

### Keep tests readable

A test should look like a test scenario rather than a collection of low-level implementation details.

### Avoid duplication

Common functionality belongs in reusable components instead of being copied between tests.

### Separate responsibilities

Pages handle UI interactions.

API classes handle API operations.

Flows handle business workflows.

Utilities handle common framework functionality.

### Make failures easier to investigate

Logs, screenshots, traces and Allure attachments should provide enough information to understand a failed execution.

### Build incrementally

The framework is intentionally being built in phases. I prefer adding an abstraction when there is a real need for it rather than creating a large framework upfront.

---

# Roadmap

### Completed

* [x] Framework setup
* [x] UI automation with Playwright
* [x] Page Object Model
* [x] Cross-browser support
* [x] Browser Factory
* [x] Configuration management
* [x] Centralized logging
* [x] Automatic screenshots on failure
* [x] API automation
* [x] API CRUD operations
* [x] API chaining
* [x] Test data factories
* [x] CSV / Excel test data support
* [x] JSON Schema validation
* [x] HTTP / Business / Contract validation
* [x] Allure reporting
* [x] Allure steps and metadata
* [x] API response attachments
* [x] Execution artifact management

### Next

* [ ] GitHub Actions CI/CD
* [ ] Allure reporting in CI
* [ ] CI artifact management
* [ ] Environment variables and secrets in CI
* [ ] Parallel execution
* [ ] Docker integration
* [ ] Database testing
* [ ] Performance testing
* [ ] Security testing
* [ ] AI-assisted test generation and maintenance

---

# Contributing

This is primarily a personal/portfolio project, but suggestions and issues are welcome.

If you see something that could make the framework cleaner, more maintainable or more reusable, feel free to open an issue or pull request.

---

# Contact

**Priya**
Senior Software Development Engineer in Test (SDET)

Automation | Playwright | Python | API Testing

* LinkedIn: [https://www.linkedin.com/in/priya-bhagoriya/](https://www.linkedin.com/in/priya-bhagoriya/)
* GitHub: [https://github.com/Priya123z](https://github.com/Priya123z)

---

# License

MIT

---