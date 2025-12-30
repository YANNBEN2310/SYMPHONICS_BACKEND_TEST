def test_post_message_ok(client):
    
    payload = {
        "bizCode": "devicePropertyMessage",
        "bizData": {
            "devId": "device123",
            "productId": "prod456",
            "dataId": "data789",
            "properties": [
                {
                    "code": "instant_power",
                    "dpId": 1,
                    "time": 1732631573782,
                    "value": 1200
                }
            ]
        },
        "ts": 1732631573782
    }

    response = client.post("/message", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["inserted_rows"] >= 0
