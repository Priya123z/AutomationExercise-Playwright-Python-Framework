import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_register_existing_user(auth_negative_flow):
    auth_negative_flow.register_an_existing_user()
