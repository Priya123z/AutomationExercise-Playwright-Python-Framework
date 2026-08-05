

def test_login(auth_api, login_request):


    response = auth_api.login(login_request)

    assert response.ok
    assert response.status == 200

    data = response.json()

    assert data["username"] == login_request.username
    assert data["accessToken"]
    assert data["refreshToken"]
