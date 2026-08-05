from models.user import User
from pages.home_page import HomePage
from utils.factories.user_factory import UserFactory


class RegisterFlow:

    def __init__(self, page):
        self.page = page

    def register(self, user: User | None = None) -> tuple[HomePage, User]:

        user = user or UserFactory.create()

        home = HomePage(self.page)

        signup = home.navbar.open_signup_login()

        account = signup.start_signup(user)

        account_created = account.create_account(user)

        return account_created.continue_to_home(), user
