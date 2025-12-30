from fastapi import APIRouter
from app.models.models import SendCommand
from app.services.pubsub_service import PubSubService

router = APIRouter()

pubsub_service = PubSubService()


@router.post("/send")
def send_cmd(command: SendCommand):
    """
    envoie une commande on/off à un device.
    """
    pubsub_service.publish_command(
        device_id=command.device_id,
        switch=command.switch
    )

    return {
        "status": "command_sent",
        "device_id": command.device_id,
        "switch": command.switch
    }
