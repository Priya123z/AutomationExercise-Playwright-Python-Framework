from pathlib import Path

import pytest

from flows.UI_Flow.login_flow import LoginFlow
from utils.test_data import TestData

filepath = Path(__file__).parent.parent.resolve()

@pytest.mark.parametrize("user",TestData.load(filepath/"test_data"/"users"/"users.json"))
def test_logout(page,user):

    login = LoginFlow(page)

    home = login.login(user["email"], user["password"])

    assert home.user_logged_in()

    signup_page = home.navbar.logout()

    signup_page.is_loaded()



