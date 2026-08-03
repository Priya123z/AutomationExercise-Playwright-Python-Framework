from models.user import User
from pages.home_page import HomePage
from utils.factories.user_factory import UserFactory


class UserManager:

    @staticmethod
    def register(page, user: User | None = None) -> tuple[HomePage, User]:

        user = user or UserFactory.create()

        home = HomePage(page)

        signup = home.navbar.open_signup_login()

        account = signup.start_signup(user)

        home = account.continue_to_home()

        return home, user