from playwright.sync_api import APIResponse

from api.api_client import APIClient
from api.endpoints import Endpoints
from models.AutomationExercise_UI_API_Models.login_response import LoginResponse
from models.AutomationExercise_UI_API_Models.register_response import RegisterResponse
from models.AutomationExercise_UI_API_Models.user import User
from utils.logger import logger


class AuthAPI:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def register(self, user: User)->tuple[APIResponse, RegisterResponse]:
        payload = {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "password": user.password,
            "title": user.title,
            "birth_date": user.date_of_birth,
            "birth_month": user.months_of_birth,
            "birth_year": user.years_of_birth,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "company": user.company,
            "address1": user.address_one,
            "address2": user.address_two,
            "country": user.country,
            "zipcode": user.zipcode,
            "state": user.state,
            "city": user.city,
            "mobile_number": user.mobile_number,
        }

        logger.info(f"Registering user: {user.first_name} {user.last_name}")


        response = self.api_client.post(
            endpoint= Endpoints.REGISTER,
            form=payload)


        body = RegisterResponse(**response.json())

        return response,body



    def verify_login(self, user: User)->tuple[APIResponse, LoginResponse]:

        payload = {
            "email": user.email,
            "password": user.password,

        }
        logger.info(f"Logging in user{user.first_name} {user.last_name}")

        response = self.api_client.post(
            endpoint=Endpoints.VERIFY_LOGIN,
            form=payload
        )

        body = LoginResponse(**response.json())

        return response,body

    def delete_user(self, user: User)->tuple[APIResponse, RegisterResponse]:
        payload = {
            "email": user.email,
            "password": user.password,
        }


        logger.info(f"Logging in user{user.first_name} {user.last_name}")

        response = self.api_client.delete(endpoint=Endpoints.DELETE_ACCOUNT,
                                          form=payload)

        body = RegisterResponse(**response.json())



        logger.info(f"Delete account request sent for {user.email}")

        return response,body

    def verify_login_with_payload(self, payload: dict) -> tuple[APIResponse, LoginResponse]:

        response = self.api_client.post(endpoint=Endpoints.VERIFY_LOGIN,
                                        form=payload)

        body = LoginResponse(**response.json())

        return response, body