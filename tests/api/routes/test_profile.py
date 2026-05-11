def test_create_profile(client, mock_external_api_calls):
    mock_external_api_calls()
    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )
    assert response.status_code == 201
    data = response.json()

    assert data["status"] == "success"
    assert data["data"]["id"] is not None
    assert data["data"]["name"] == "mike"


def test_idempotency(client, mock_external_api_calls):
    mock_external_api_calls()
    client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )
    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_get_profile(client, mock_external_api_calls):
    mock_external_api_calls()
    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )
    profile_id = response.json()["data"]["id"]
    response = client.get(
        url=f"/api/profiles/{profile_id}"
    )

    assert response.status_code == 200
    data = response.json()

    assert data["data"]["id"] == profile_id
    assert data["data"]["name"] == "mike"


def test_get_all_profiles(client, mock_external_api_calls):
    mock_external_api_calls()

    client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    client.post(
        url="/api/profiles",
        json={"name": "james"}
    )
    response = client.get(
        url="/api/profiles"
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data["data"]) == 2


def test_delete_profile(client, mock_external_api_calls):
    mock_external_api_calls()

    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )
    profile_id = response.json()["data"]["id"] 

    response = client.delete(
        url = f"/api/profiles/{profile_id}"
    )

    assert response.status_code == 204


def test_agify_edge_case(client, mock_external_api_calls):
    agify_data = {
        "count": 147558,
        "name": "mike",
    }
    mock_external_api_calls(agify_data=agify_data)

    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    assert response.status_code == 502
    
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Agify returned an invalid response."


def test_genderize_count_edge_case(client, mock_external_api_calls):
    genderize_data = {
        "count": 0,
        "name": "mike",
        "gender": "male",
        "probability": 1
    }
    mock_external_api_calls(genderize_data=genderize_data)

    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    assert response.status_code == 502
    
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Genderize returned an invalid response."


def test_genderize_gender_edge_case(client, mock_external_api_calls):
    genderize_data = {
        "count": 12345,
        "name": "mike",
        "probability": 1
    }
    mock_external_api_calls(genderize_data=genderize_data)

    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    assert response.status_code == 502
    
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Genderize returned an invalid response."


def test_nationalize_edge_case(client, mock_external_api_calls):
    nationalize_data = {
        "count": 311532,
        "name": "mike"
    }
    mock_external_api_calls(nationalize_data=nationalize_data)

    response = client.post(
        url="/api/profiles",
        json={"name": "mike"}
    )

    assert response.status_code == 502
    
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Nationalize returned an invalid response."
