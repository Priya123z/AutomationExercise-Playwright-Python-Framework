import pytest

@pytest.mark.api
@pytest.mark.auth
def test_register_and_verify_delete_account(auth_flow):

    user, body = auth_flow.register_and_verify_delete()

    assert body.responseCode == 200

    assert body.message == "Account deleted!"
