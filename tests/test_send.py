def test_send_command_ok(client):
    payload = {
        "device_id": "device123",
        "switch": True
    }

    response = client.post("/send", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "command_sent"
    assert body["device_id"] == "device123"
    assert body["switch"] is True
