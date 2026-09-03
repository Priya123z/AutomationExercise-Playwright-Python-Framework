import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_verify_login_with_unregistered_user(auth_negative_flow):

    auth_negative_flow.verify_login_with_unregistered_user()
