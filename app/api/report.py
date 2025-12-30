from fastapi import APIRouter
from app.services.sqlite_service import SQLiteService

router = APIRouter()

sqlite_service = SQLiteService()


@router.get("/report/power")
def get_power_report():
    """
    return un rapport agrégé des consommations électriques
    par jour et par créneau horaire.
    """
    return sqlite_service.get_power_report()


@router.get("/report/temperature")
def get_temperature_report():
    """
    return un rapport agrégé des temperatures
    par jour et par créneau horaire.
    """
    return sqlite_service.get_temperature_report()
