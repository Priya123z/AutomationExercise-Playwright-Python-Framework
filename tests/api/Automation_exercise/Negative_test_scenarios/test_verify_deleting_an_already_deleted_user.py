import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.negative
def test_deleting_an_already_deleted_user(auth_negative_flow):
    auth_negative_flow.verify_delete_with_a_deleted_account()
