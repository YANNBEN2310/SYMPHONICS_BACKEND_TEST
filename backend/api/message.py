from fastapi import APIRouter, HTTPException
from backend.models.models import DeviceMessage
from backend.services.sqlite_service import SQLiteService
from backend.services.device_memory import DeviceStateCache

router = APIRouter()

sqlite_service = SQLiteService()
device_cache = DeviceStateCache()

ALLOWED_CODES = {"instant_power", "temp_interior"}


@router.post("/message")
def receive_device_message(message: DeviceMessage):
    """
    Réception des messages envoyés par les appareils connectés.
    Seules les propriétés ayant changé sont persistées.
    """

    if message.bizCode != "devicePropertyMessage":
        raise HTTPException(
            status_code=400,
            detail="Type de message non supporté"
        )

    rows_to_insert = []

    for prop in message.bizData.properties:
        if prop.code not in ALLOWED_CODES:
            continue

        has_changed = device_cache.has_changed(
            dev_id=message.bizData.devId,
            code=prop.code,
            new_value=prop.value
        )

        if has_changed:
            rows_to_insert.append({
                "dev_id": message.bizData.devId,
                "product_id": message.bizData.productId,
                "code": prop.code,
                "value": prop.value,
                "time": prop.time
            })

    if rows_to_insert:
        sqlite_service.insert_rows(rows_to_insert)

    return {
        "status": "ok",
        "inserted_rows": len(rows_to_insert)
    }
