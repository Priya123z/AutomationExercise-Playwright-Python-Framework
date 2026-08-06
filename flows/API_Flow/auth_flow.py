from api.auth_api import AuthAPI
from utils.factories.user_factory import UserFactory
from utils.schema_validator import SchemaValidator


class AuthFlow:

    def __init__(self, auth_api: AuthAPI):
        self.auth_api = auth_api

    def register_and_verify_user(self):

        user = UserFactory.create()
        response,register_body = self.auth_api.register(user)
        # 1. HTTP Validation
        assert response.status == 200

        # 2. Business Validation
        assert register_body.responseCode == 201
        assert register_body.message == "User created!"

        # 3. Contract Validation
        SchemaValidator.validate_response(response,"schemas/auth/create_user_schema.json")
        return user

    def register_and_verify_login(self):

        user= self.register_and_verify_user()

        response,login_body = self.auth_api.verify_login(user)

        # 1. HTTP Validation
        assert response.status == 200

        # 2. Business Validation
        assert login_body.responseCode == 200
        assert login_body.message == "User exists!"

        #3. Contract validation
        SchemaValidator.validate_response(response,"schemas/auth/login_user_schema.json")
        return user

    def register_and_verify_delete(self):
        user = self.register_and_verify_login()

        response, delete_body = self.auth_api.delete_user(user)

        # 1. HTTP Validation
        assert response.status == 200

        # 2. Business Validation
        assert delete_body.responseCode == 200
        assert delete_body.message == "Account deleted!"

        #3. Contract Validation
        SchemaValidator.validate_response(response,"schemas/auth/delete_user_schema.json")
        return user, delete_body




