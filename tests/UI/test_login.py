from pathlib import Path
import pytest
from models.AutomationExercise_UI_API_Models.user import User
from pages.home_page import HomePage
from utils.test_data import TestData

filepath = Path(__file__).parent.parent.resolve()

users = TestData.load(filepath /"test_data/users/users.json", model=User)
# users -> list[User]

@pytest.mark.parametrize("user",users)
def test_login_user(page, user):

    home = HomePage(page)
    signup_login = home.navbar.open_signup_login()
    signup_login.login(user.email, user.password)



