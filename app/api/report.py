from fastapi import APIRouter
from app.services.sqlite_service import SQLiteService

router = APIRouter()

sqlite_service = SQLiteService()


@router.get("/report")
def get_report():
    """
    return un rapport agrégé des consommations électriques
    par jour et par créneau horaire.
    """
    return sqlite_service.get_power_report()
