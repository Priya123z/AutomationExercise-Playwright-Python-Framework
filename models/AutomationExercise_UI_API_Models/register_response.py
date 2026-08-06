from dataclasses import dataclass


@dataclass
class RegisterResponse:
    responseCode: int
    message: str