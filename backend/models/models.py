from typing import List
from pydantic import BaseModel, Field

class Property(BaseModel):
    """
    Ppropriété d'un appareil connecté.
    puissance instantanée, température intérieure.
    """
    code: str  # identifiant la propriete (code: "instant_power")
    dpId: int  # identifiant numérique du point
    time: int  # horodatage en ms
    value: float  # Valeur numérique de la propriété (value: 2500 watts)

class BizData(BaseModel):
    """
    Contient les données principales d'un message envoyé par un appareil.
    """
    devId: str  # identifiant unique de l'appareil
    productId: str  # identifiant du modèle de l'appareil
    dataId: str  # identifiant unique du message
    properties: List[Property]  # liste des propriétés envoyées par l'appareil

class DeviceMessage(BaseModel):
    """
    Modéliser le message complet reçu depuis un appareil.
    """
    bizCode: str  # code pour identifier le type de message
    bizData: BizData  # data principales du message
    ts: int  # horodatage global du message

class SendCommand(BaseModel):
    """
    Modéliser une commande à envoyer à un appareil (on/off).
    """
    device_id: str = Field(..., min_length=1)  # Identifiant de l'appareil (ne peut pas être vide)
    switch: bool  # Bool pour activerou désactiver l'appareil
