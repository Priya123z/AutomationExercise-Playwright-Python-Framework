# Automation Exercise-Playwright-Python

A production-ready UI and API automation framework built with Playwright and Python.
What started as a collection of automation scripts gradually evolved into a maintainable framework as the project grew in size and complexity. This repository reflects that journey, focusing on scalability, reusability, and clean architecture rather than simply automating test cases.

## Why this exists

Writing automated tests is easy. Keeping a growing suite maintainable is not. 
As the number of scripts increased, so did the duplication, the flaky fixtures, and the time spent fixing broken tests instead of writing new ones. This framework is an attempt to fix that by separating concerns properly: pages, flows, data, and configuration all live in their own place instead of being tangled together.

## Tech stack

- **Playwright** - browser automation
- **Python** - core language
- **Pytest** - test runner and fixtures
- **Page Object Model** - UI structure
- **Playwright API** - REST API testing

## Project structure

                    Test Cases
                         │
                         ▼
                 Business Flows
                         │
                         ▼
                  Page Objects
                         │
                         ▼
               Playwright / API Layer
                         │
                         ▼
                  Browser Factory

```
AutomationExercise-Playwright-Python/
├── api/            # API clients & utilities
├── config/         # Configuration & environment management
├── flows/          # Business/user flows built on top of pages
├── models/         # Data models
├── pages/          # Page Object Models
├── tests/          # Test cases
├── test_data/      # Test data & payloads
├── utils/          # Reusable utilities (browser factory, logger, etc.)
├── reports/        # Test reports
└── artifacts/      # Screenshots, logs, traces
```

## Getting started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/Priya123z/AutomationExercise-Playwright-Python.git
cd AutomationExercise-Playwright-Python
pip install -r requirements.txt
playwright install
```

### Running the tests

```bash
# run the full suite
pytest

# run a specific test file
pytest tests/test_login.py

# run with a specific browser
pytest --browser=firefox

# run in headed mode (useful for debugging)
pytest --headed
```

### Configuration

Environment-specific settings (base URLs, credentials, timeouts) are managed through `config/`. Copy `config/.env.example` to `config/.env` and fill in the values for your environment before running the suite.


## Features

- UI Automation using Playwright
- REST API CRUD Testing
- Cross-browser execution
- Browser Factory
- Page Object Model
- Environment-based configuration
- Centralized logging
- Automatic screenshots on failures
- Reusable business flows
- Modular project architecture


## What's included

- UI automation with Playwright's sync API
- API testing with Pytest, covering CRUD flows
- A `ConfigManager` for environment-based configuration
- A `BrowserFactory` for cross-browser execution
- Centralized logging and automatic screenshots on failure
- Reusable components across both UI and API layers

## Design principles

- **Scalability** - code structure and abstraction should make it easy to add new tests without touching existing ones
- **Maintainability** - clean code, consistent naming, and no copy-pasted logic
- **Reusability** - anything written once (a page, a flow, a utility) should be usable across the whole suite, and ideally across other projects too

## Roadmap

- [x] Framework setup
- [x] UI automation with Playwright
- [x] Cross browser support 
- [x] Configuration management
- [x] Logging
- [x] Screenshots
- [x] API automation (CRUD)
- [ ] API chaining across multi-step flows
- [ ] JSON schema validation for API responses
- [ ] Database testing
- [ ] GitHub Actions CI/CD pipeline
- [ ] Docker integration
- [ ] Allure reporting
- [ ] AI-assisted test generation and maintenance

## Contributing

This is primarily a personal/portfolio project, but suggestions and issues are welcome. If you spot something that could be cleaner or more reusable, open an issue or a PR.

## Contact

**Priya** - Senior Software Development Engineer in Test (SDET)
            Automation | Playwright | Python | API Testing

- LinkedIn: [https://www.linkedin.com/in/priya-bhagoriya/](https://www.linkedin.com/in/priya-bhagoriya/)
- GitHub: [github.com/Priya123z](https://github.com/Priya123z)

## License

MIT