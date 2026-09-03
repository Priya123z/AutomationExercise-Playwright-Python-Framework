import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_login_with_invalid_password(auth_negative_flow):

  auth_negative_flow.verify_login_with_invalid_password()
