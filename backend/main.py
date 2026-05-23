from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, servidores, cargas
from app.core.config import settings

app = FastAPI(
    title="Aurea Finance API",
    description="Plataforma de Carga y Gestión de Datos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,       prefix="/api/auth",       tags=["Autenticación"])
app.include_router(servidores.router, prefix="/api/servidores", tags=["Servidores"])
app.include_router(cargas.router,     prefix="/api/cargas",     tags=["Cargas"])


@app.get("/")
def root():
    return {"message": "Aurea Finance API activa"}
