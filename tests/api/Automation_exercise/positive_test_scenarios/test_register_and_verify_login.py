import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.smoke
def test_register_and_verify_login(auth_flow):

    auth_flow.register_and_verify_login()



