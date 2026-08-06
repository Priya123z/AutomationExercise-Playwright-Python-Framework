
from pages.home_page import HomePage
from utils.factories.user_factory import UserFactory

import allure


@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Register a new user successfully")
@allure.description("Verify that a new user can be registered using valid details.")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup(page):

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
    home.navbar.logout()




