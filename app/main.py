from fastapi import FastAPI
from app.api.message import router as message_router
from app.api.send import router as send_router
from app.api.report import router as report_router

app = FastAPI(
    title="IoT Energy API",
    description="API de gestion de consommation énergétique des appareils connectés",
    version="1.0.0"
)

app.include_router(message_router)
app.include_router(send_router)
app.include_router(report_router)
