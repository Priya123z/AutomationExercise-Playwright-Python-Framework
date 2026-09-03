import pytest
import allure

from pages.home_page import HomePage


@allure.title("Login with valid credentials")
@allure.description("Verify that a registered user can log in with valid details.")
@allure.feature("Authentication")
@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.smoke
def test_login_user(page, registered_user):
    home = HomePage(page)

    signup_login = home.navbar.open_signup_login()
    signup_login.login(registered_user.email, registered_user.password)

    assert home.user_logged_in()
