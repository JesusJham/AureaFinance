from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import data_entries
from app.api.routes import auth, servidores, cargas
from app.core.database import engine, Base
import app.models.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aurea Finance API",
    description="Plataforma de Carga y Gestión de Datos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(servidores.router, prefix="/api/servidores", tags=["Servidores"])
app.include_router(cargas.router, prefix="/api/cargas", tags=["Cargas"])
app.include_router(
    data_entries.router,
    prefix="/api/data-entries",
    tags=["Data Entries"]
)

@app.get("/")
def root():
    return {"message": "Aurea Finance API activa"}