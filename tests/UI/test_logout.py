import pytest

from flows.UI_Flow.login_flow import LoginFlow


@pytest.mark.ui
@pytest.mark.auth
def test_logout(page, registered_user):
    login = LoginFlow(page)

    home = login.login(registered_user.email, registered_user.password)

    assert home.user_logged_in()

    signup_page = home.navbar.logout()

    signup_page.is_loaded()
