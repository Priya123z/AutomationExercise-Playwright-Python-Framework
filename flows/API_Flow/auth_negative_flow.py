from multiprocessing.context import assert_spawning

from api.auth_api import AuthAPI
from flows.API_Flow import auth_flow
from flows.API_Flow.auth_flow import AuthFlow
from utils.factories.user_factory import UserFactory


class AuthNegativeFlow:
    def __init__(self, auth_api: AuthAPI, auth_flow: AuthFlow):
        self.auth_api = auth_api
        self.auth_flow = auth_flow


    def verify_login_with_invalid_password(self):
        user = self.auth_flow.register_and_verify_user()
        user.password = "InvalidPassword123"
        _,login_body = self.auth_api.verify_login(user)

        assert login_body.responseCode == 404
        assert login_body.message == "User not found!"

    def verify_login_with_unregistered_user(self):
        user = UserFactory.create()

        # Don't register

        _,login_body = self.auth_api.verify_login(user)

        assert login_body.responseCode == 404
        assert login_body.message == "User not found!"

    def register_an_existing_user(self):

        user = self.auth_flow.register_and_verify_user()

        _,register_body = self.auth_api.register(user)

        assert register_body.responseCode == 400
        assert register_body.message == "Email already exists!"

        return register_body

    def login_with_empty_email(self):
        payload = {
            "password": "Password@123"
        }
        _,login_body = self.auth_api.verify_login_with_payload(payload)

        assert login_body.responseCode == 400
        assert login_body.message == "Bad request, email or password parameter is missing in POST request."
        return login_body

    def login_with_empty_password(self):
        payload = {
            "email": "abc@test.com"
        }
        _,login_body = self.auth_api.verify_login_with_payload(payload)
        assert login_body.responseCode == 400
        assert login_body.message == "Bad request, email or password parameter is missing in POST request."
        return login_body

    def verify_login_with_missing_credentials(self):
        payload = {}

        _, login_body = self.auth_api.verify_login_with_payload(payload)

        assert login_body.responseCode == 400
        assert login_body.message == "Bad request, email or password parameter is missing in POST request."



    def verify_delete_with_a_deleted_account(self):

        user = self.auth_flow.register_and_verify_user()

        # First delete should succeed
        _,delete_body = self.auth_api.delete_user(user)

        assert delete_body.responseCode == 200
        assert delete_body.message == "Account deleted!"


        _,delete_body = self.auth_api.delete_user(user)
        # Second Delete should throw an error

        assert delete_body.responseCode == 404
        assert delete_body.message == "Account not found!"
        return user,delete_body














