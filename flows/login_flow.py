from pages.base_page import BasePage
from pages.home_page import HomePage


class LoginFlow(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def login(self, username, password):
        home = HomePage(self.page)
        signup_login = home.navbar.open_signup_login()
        return signup_login.login(username, password)

