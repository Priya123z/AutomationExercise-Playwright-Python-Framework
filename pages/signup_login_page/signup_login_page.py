from models.user import User
from pages.base_page import BasePage


class SignUpLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        #components

        #page headings
        self._signup_heading = page.get_by_role("heading",name="New User Signup!")
        self._login_heading = page.get_by_role("heading",name="Login to your account")

        # Signup section
        self._signup_name = page.locator("[data-qa='signup-name']")
        self._signup_email = page.locator("[data-qa='signup-email']")
        self._signup_button = page.locator("[data-qa='signup-button']")

        #login section
        self._login_email = page.locator("[data-qa='login-email']")
        self._login_password = page.locator("[data-qa='login-password']")
        self._login_button = page.locator("[data-qa='login-button']")


    def is_loaded(self)->None:
        self.wait_for_visibility(self._login_heading,"Login Heading")
        self.wait_for_visibility(self._signup_heading,"Signup Heading")

    def _fill_login_email(self,email:str):
        self.fill(self._login_email,value=email,description="Login Email")
    def _fill_login_password(self,password:str):
        self.fill(self._login_password,value=password,description="Login Password")
    def _click_login_button(self):
        self.click(self._login_button, "Click on Login Button")
    def _fill_signup_name(self,name:str):
        self.fill(self._signup_name,value=name,description="Signup Name")
    def _fill_signup_email(self,email:str):
        self.fill(self._signup_email,value=email,description="Signup Email")
    def _click_signup_button(self):
        self.click(self._signup_button,"Click on Signup")

    def login(self,email: str, password: str)->HomePage:
        from pages.home_page import HomePage

        self._fill_login_email(email)
        self._fill_login_password(password)
        self._click_login_button()
        home = HomePage(self.page)
        home.is_loaded()
        return home

    def start_signup(self,user:User):
        from pages.signup_login_page.signup_page import SignupPage
        self._fill_signup_name(user.first_name)
        self._fill_signup_email(user.email)
        self._click_signup_button()
        signup_page = SignupPage(self.page)
        signup_page.is_loaded()
        return signup_page


