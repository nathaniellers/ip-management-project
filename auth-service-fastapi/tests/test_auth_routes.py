from fastapi import status

def test_login_token_success(client):
	response = client.post("/api/token", data={
		"username": "nathanielleromero18@gmail.com",
		"password": "mysecretpass"
	})
	assert response.status_code == 200
	json = response.json()
	assert "access_token" in json
	assert json["token_type"] == "bearer"


def test_login_token_invalid_credentials(client):
	response = client.post("/api/token", data={
		"username": "nathanielleromero18@gmail.com",
		"password": "wrongpass"
})
	assert response.status_code == status.HTTP_401_UNAUTHORIZED
	assert response.json()["detail"] == "Incorrect credentials"


def test_login_user_success(client):
	response = client.post("/api/login", json={
		"email": "nathanielleromero18@gmail.com",
		"password": "mysecretpass"
	})
	assert response.status_code == 200
	json = response.json()
	assert "access_token" in json
	assert json["token_type"] == "bearer"


def test_login_user_invalid(client):
	response = client.post("/api/login", json={
		"email": "nathanielleromero18@gmail.co",
		"password": "badpass"
	})
	assert response.status_code == 401


def test_protected_route_requires_token(client):
	response = client.post("/api/test-protected")
	assert response.status_code == 401


def test_protected_route_with_token(client):
	login_response = client.post("/api/token", data={
		"username": "nathanielleromero18@gmail.com",
		"password": "mysecretpass"
	})
	token = login_response.json()["access_token"]

	protected_response = client.post(
		"/api/test-protected",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert protected_response.status_code == 200
	assert protected_response.json()["email"] == "nathanielleromero18@gmail.com"


def test_logout_success(client):
	login_response = client.post("/api/token", data={
		"username": "nathanielleromero18@gmail.com",
		"password": "mysecretpass"
	})
	token = login_response.json()["access_token"]

	logout_response = client.post(
		"/api/logout",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert logout_response.status_code == 200
	assert logout_response.json()["message"] == "Successfully logged out."


def test_logout_twice(client):
	login_response = client.post("/api/token", data={
		"username": "nathanielleromero18@gmail.com",
		"password": "mysecretpass"
	})
	token = login_response.json()["access_token"]

	first = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
	assert first.status_code == 200

	second = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
	assert second.status_code == 400
	assert "Token already blacklisted" in second.text

# def test_refresh_token_flow(client):
#     login_response = client.post("/api/login", json={
#         "email": "nathanielleromero18@gmail.com",
#         "password": "mysecretpass"
#     })
#     refresh_token = login_response.json().get("refresh_token")
#     assert refresh_token

#     refresh_response = client.post("/api/refresh", json={"refresh_token": refresh_token})
#     assert refresh_response.status_code == 200
#     assert "access_token" in refresh_response.json()
