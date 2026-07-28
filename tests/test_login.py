from pathlib import Path

import pytest

from pages.home_page import HomePage
from utils.test_data import TestData
from utils.factories.reader_factory import ReaderFactory


filepath = Path(__file__).parent.parent.resolve()

@pytest.mark.parametrize("user",TestData.load(filepath/"test_data"/"users"/"users.json"))
def test_login_user(page, user):

    home = HomePage(page)
    signup_login = home.navbar.open_signup_login()
    signup_login.login(user["email"],user["password"])



