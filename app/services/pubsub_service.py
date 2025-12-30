import json
from app.configs.config import settings


class PubSubService:
    """
    service d'envoi de commandes aux devcies.
   enlocal, je simule l'envoi pub/sub.
    """

    def publish_cmd(self, device_id: str, switch: bool) -> None:
        message = {
            "devId": device_id,
            "switch": switch
        }

        if settings.ENV == "local":
            # simulation locale
            print(f"[PUBSUB - LOCAL] Topic={settings.PUBSUB_TOPIC} | Message={json.dumps(message)}")
            return

        # en prod, ici on utiliserait google-cloud-pubsub
        # publisher.publish(...)
