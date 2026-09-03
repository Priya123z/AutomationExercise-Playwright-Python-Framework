import pytest

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.smoke
def test_login(dummyjson_auth_api, login_request):

    response = dummyjson_auth_api.login(login_request)

    assert response.ok
    assert response.status == 200

    data = response.json()

    assert data["username"] == login_request.username
    assert data["accessToken"]
    assert data["refreshToken"]
