
from pages.home_page import HomePage
from utils.factories.user_factory import UserFactory

import allure


@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Register a new user successfully")
@allure.description("Verify that a new user can be registered using valid details.")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup(page):

    with allure.step("Create test user"):
        user = UserFactory.create()

    home = HomePage(page)

    with allure.step("Open Signup/Login page"):
        signup_login = home.navbar.open_signup_login()
        signup_login.is_loaded()

    with allure.step("Start signup"):
        signup_page = signup_login.start_signup(user)
        signup_page.is_loaded()

    with allure.step("Create account"):
        account_created = signup_page.create_account(user)
        account_created.is_loaded()

    with allure.step("Continue to home"):

        home = account_created.continue_to_home()

    with allure.step("Verify user is logged in"):

        assert home.user_logged_in()
    with allure.step("Logging out the user"):
        home.navbar.logout()




