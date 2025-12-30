def test_get_report(client):
    response = client.get("/report")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
