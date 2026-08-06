from pathlib import Path
import pytest
from models.AutomationExercise_UI_API_Models.user import User
from pages.home_page import HomePage
from utils.test_data import TestData
import allure

filepath = Path(__file__).parent.parent.parent.resolve()

users = TestData.load(filepath /"test_data/users/users.json", model=User)
# users -> list[User]

@allure.title("Login with valid credentials")
@allure.description("Verify that a user can successfully login with valid details.")
@allure.feature("Authentication")

@pytest.mark.parametrize("user",users)
def test_login_user(page, user):

    home = HomePage(page)
    signup_login = home.navbar.open_signup_login()
    signup_login.login(user.email, user.password)



