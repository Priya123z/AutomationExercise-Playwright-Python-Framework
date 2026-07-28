
from pages.home_page import HomePage
from utils.factories.user_factory import UserFactory


def test_signup(page):

    user = UserFactory.create()

    home = HomePage(page)

    signup_login = home.navbar.open_signup_login()

    signup_page = signup_login.start_signup(user)

    account_created = signup_page.create_account(user)

    home = account_created.continue_to_home()

    home.navbar.logout()




