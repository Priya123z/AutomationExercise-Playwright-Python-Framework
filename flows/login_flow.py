from pages.home_page import HomePage


class LoginFlow:

    def __init__(self, page):
        self.home = HomePage(page)

    def login(self, username, password):
        signup_login = self.home.navbar.open_signup_login()
        return signup_login.login(username, password)