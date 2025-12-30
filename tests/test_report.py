def test_get_power_report(client):
    response = client.get("/report/power")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_temperature_report(client):
    response = client.get("/report/temperature")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
