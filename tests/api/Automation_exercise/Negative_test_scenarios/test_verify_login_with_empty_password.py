import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_verify_login_with_empty_password(auth_negative_flow):
    auth_negative_flow.login_with_empty_password()
