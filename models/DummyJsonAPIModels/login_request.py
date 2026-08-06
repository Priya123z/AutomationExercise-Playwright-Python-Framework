from dataclasses import dataclass


@dataclass(slots=True)
class LoginRequest:
    username: str
    password: str
