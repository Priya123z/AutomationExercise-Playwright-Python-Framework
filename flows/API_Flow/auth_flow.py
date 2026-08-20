import allure

from api.auth_api import AuthAPI
from utils.factories.user_factory import UserFactory
from utils.schema_validator import SchemaValidator


class AuthFlow:

    def __init__(self, auth_api: AuthAPI):
        self.auth_api = auth_api


    @allure.feature("Authentication")
    @allure.story("User Registration")
    @allure.title("Register a new user successfully")
    @allure.description("Verify that a new user can be registered using valid details.")
    @allure.severity(allure.severity_level.CRITICAL)

    def register_and_verify_user(self):

        with allure.step("Create test user"):
            user = UserFactory.create()

        with allure.step("Register user"):

            response,register_body = self.auth_api.register(user)

        with allure.step("Validating HTTP Response"):
            # 1. HTTP Validation
            assert response.status == 200

        with allure.step("Validating business response"):
            # 2. Business Validation
            allure.attach(response.text(),name="Register API Response",attachment_type=allure.attachment_type.JSON)
            assert register_body.responseCode == 201
            assert register_body.message == "User created!"

        with allure.step("Validating JSON Schema"):
            # 3. Contract Validation
            SchemaValidator.validate_response(response,"schemas/auth/create_user_schema.json")
            return user


    @allure.feature("Authentication")
    @allure.story("User Login")
    @allure.title("Login with a registered user")
    @allure.description("Verify that a registered user can successfully log in.")
    @allure.severity(allure.severity_level.CRITICAL)
    def register_and_verify_login(self):

        with allure.step("Register and Verify User"):

            user= self.register_and_verify_user()

        with allure.step("Login with registered user"):
            response,login_body = self.auth_api.verify_login(user)

        with allure.step("Validating HTTP Response"):
            # 1. HTTP Validation
            assert response.status == 200
        with allure.step("Validating business response"):
            allure.attach(response.text(),name="Login API response",attachment_type=allure.attachment_type.JSON)
            # 2. Business Validation
            assert login_body.responseCode == 200
            assert login_body.message == "User exists!"

        with allure.step("Validating JSON Schema"):
            #3. Contract validation
            SchemaValidator.validate_response(response,"schemas/auth/login_user_schema.json")
            return user

    @allure.feature("Authentication")
    @allure.story("Delete Account")
    @allure.title("Delete registered user successfully")
    @allure.description("Verify that a registered user can successfully delete their account.")
    @allure.severity(allure.severity_level.CRITICAL)
    def register_and_verify_delete(self):

        with allure.step("Register and login user"):
            user = self.register_and_verify_login()

        with allure.step("Delete user account"):
            response, delete_body = self.auth_api.delete_user(user)

        with allure.step("Validate HTTP response"):
            assert response.status == 200

        with allure.step("Validate business response"):
            allure.attach(response.text(),name="Deleting User API response",attachment_type=allure.attachment_type.JSON)
            assert delete_body.responseCode == 200
            assert delete_body.message == "Account deleted!"

        with allure.step("Validate JSON schema"):
            SchemaValidator.validate_response(response,"schemas/auth/delete_user_schema.json")
        return user, delete_body




