from dataclasses import dataclass


@dataclass
class LoginResponse:
    responseCode: int
    message: str