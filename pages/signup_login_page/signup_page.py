from pathlib import Path


from pages.base_page import BasePage
from pages.signup_login_page.account_created_page import AccountCreatedPage
from models.AutomationExercise_UI_API_Models.user import User
from utils.factories.writer_factory import WriterFactory

file_path = Path(__file__).parent.parent.parent.resolve()


class SignupPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        #account header
        self._account_heading = page.get_by_role("heading",name ="Enter Account Information")

        #Account Information
        self._password = page.locator("[data-qa='password']")
        self._day_dropdown = page.locator("[data-qa = 'days']")
        self._month_dropdown = page.locator("[data-qa = 'months']")
        self._year_dropdown = page.locator("[data-qa = 'years']")
        self._newsletter_checkbox = page.get_by_role("checkbox",name ="newsletter")
        self._special_offers_checkbox = page.locator("#newsletter")
        self._firstname = page.locator("#first_name")
        self._lastname = page.locator("#last_name")
        self._company = page.locator("#company")
        self._address_one = page.locator("[data-qa='address']")
        self._address_two = page.locator("[data-qa='address2']")
        self._country = page.locator("#country")
        self._state = page.locator("[data-qa='state']")
        self._city = page.locator("[data-qa='city']")
        self._zipcode = page.locator("[data-qa='zipcode']")
        self._mobile = page.locator("#mobile_number")
        self._create_account_button = page.locator("[data-qa='create-account']")

    def _select_title(self,title:str):
        self.click(self.page.locator(f".radio-inline [value='{title}']"),f"Selecting {title}")
    def _fill_password(self,password):
        self.fill(self._password,password,"entering password")
    def _select_date_of_birth(self,day:str):
        self.select_option(self._day_dropdown, day, description="selecting dateOfBirth")
    def _select_months_of_birth(self,month:str):
        self.select_option(self._month_dropdown,month, description="selecting monthsOfBirth")
    def _select_years_of_birth(self,year:str):
        self.select_option(self._year_dropdown,year,"selecting years")

    def _check_newsletter(self,subscribe:bool):
        if subscribe:
            self.click(self._newsletter_checkbox,"Subscribing newsletters")

    def _check_special_offers(self,check_special_offers:bool):
        if check_special_offers:
            self.click(self._special_offers_checkbox,"Special Offers")

    def _fill_first_name(self,firstname:str):
        self.fill(self._firstname,firstname,"First name")
    def _fill_last_name(self,lastname:str):
        self.fill(self._lastname,lastname,"Last name")
    def _fill_company (self,company:str):
        self.fill(self._company,company,"Company")
    def _fill_address_one(self,address_one):
        self.fill(self._address_one,address_one,"Address line 1")
    def _fill_address_two(self,address_two):
        self.fill(self._address_two,address_two,"Address line 2")
    def _select_country(self,country):
        self.select_option(self._country,country,"Select country")
    def _fill_state(self,state):
        self.fill(self._state,state,"Select state")
    def _fill_city(self,city):
        self.fill(self._city,city,"Select city")
    def _fill_zipcode(self,zipcode):
        self.fill(self._zipcode,zipcode,"Select zipcode",)
    def _fill_mobile(self,mobile):
        self.fill(self._mobile,mobile,"Select mobile",)
    def _click_create_account(self):
        self.click(self._create_account_button,"Create account button click")


    def create_account(self, user:User)->AccountCreatedPage:
        self._select_title(user.title)
        self._fill_password(user.password)
        self._select_date_of_birth(user.date_of_birth)
        self._select_months_of_birth(user.months_of_birth)
        self._select_years_of_birth(user.years_of_birth)
        self._check_special_offers(user.special_offers)
        self._check_newsletter(user.newsletter)
        self._fill_first_name(user.first_name)
        self._fill_last_name(user.last_name)
        self._fill_company(user.company)
        self._fill_address_one(user.address_one)
        self._fill_address_two(user.address_two)
        self._select_country(user.country)
        self._fill_state(user.state)
        self._fill_city(user.city)
        self._fill_zipcode(user.zipcode)
        self._fill_mobile(user.mobile_number)
        self._click_create_account()
        account_created_page = AccountCreatedPage(self.page)
        account_created_page.is_loaded()
        writer = WriterFactory.get_writer(file_path/"test_data"/"users"/"users.json")
        writer.append(file_path/"test_data"/"users"/ "users.json", user)
        return account_created_page

    def is_loaded(self):
        self.wait_for_visibility(self._account_heading,"Signup section loaded")


