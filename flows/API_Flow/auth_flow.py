from api.auth_api import AuthAPI
from utils.factories.user_factory import UserFactory


class AuthFlow:

    def __init__(self, auth_api: AuthAPI):
        self.auth_api = auth_api

    def register_and_verify_user(self):

        user = UserFactory.create()
        _,register_body = self.auth_api.register(user)
        assert register_body.responseCode == 201
        assert register_body.message == "User created!"
        return user

    def register_and_verify_login(self):

        user= self.register_and_verify_user()

        _,login_body = self.auth_api.verify_login(user)

        assert login_body.responseCode == 200
        assert login_body.message == "User exists!"

        return user

    def register_and_verify_delete(self):
        user = self.register_and_verify_login()

        _, delete_body = self.auth_api.delete_user(user)

        assert delete_body.responseCode == 200
        assert delete_body.message == "Account deleted!"

        return user, delete_body




