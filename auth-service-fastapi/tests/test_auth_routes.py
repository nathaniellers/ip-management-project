from fastapi import status
import uuid

def test_register_user(client):
	random_email = f"{uuid.uuid4().hex[:10]}@yopmail.com"
	random_name = f"Test-{uuid.uuid4().hex[:6]}"

	response = client.post("/api/register", json={
		"email": random_email,
		"password": "password",
		"full_name": random_name
	})

	print("Status Code:", response.status_code)
	print("Response Body:", response.text)

	assert response.status_code in [200, 201]
	json_response = response.json()
	assert json_response["email"] == random_email
	assert json_response["full_name"] == random_name

def test_login_user_success(client):
	response = client.post("/api/login", json={
		"email": "nathanielleromero18@gmail.com",
		"password": "password"
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

def test_logout_success(client):
	login_response = client.post("/api/login", json={
		"email": "nathanielleromero18@gmail.com",
		"password": "password"
	})

	token = login_response.json()["access_token"]

	logout_response = client.post(
		"/api/logout",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert logout_response.status_code == 200
	assert logout_response.json()["message"] == "Successfully logged out."


def test_logout_twice(client):
	login_response = client.post("/api/login", json={
		"email": "nathanielleromero18@gmail.com",
		"password": "password"
	})
	token = login_response.json()["access_token"]

	first = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
	assert first.status_code == 200

	second = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
	assert second.status_code == 400
	assert "Token already blacklisted" in second.text

