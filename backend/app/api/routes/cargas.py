from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.models.models import Carga
from app.schemas.schemas import CargaCreate, CargaOut
from app.services.carga_service import validar_archivo, ejecutar_carga

router = APIRouter()


@router.get("/", response_model=List[CargaOut])
def listar_cargas(db: Session = Depends(get_db)):
    return db.query(Carga).order_by(Carga.created_at.desc()).all()


@router.post("/", response_model=CargaOut, status_code=201)
def crear_carga(data: CargaCreate, db: Session = Depends(get_db)):
    carga = Carga(**data.model_dump())
    db.add(carga)
    db.commit()
    db.refresh(carga)
    return carga


@router.post("/validar")
async def validar(
    file: UploadFile = File(...),
    separador: Optional[str] = Form(","),
    codificacion: Optional[str] = Form("UTF-8"),
):
    """Valida el archivo y retorna preview de columnas."""
    contenido = await file.read()
    resultado = validar_archivo(contenido, file.filename, separador, codificacion)
    return resultado


@router.post("/{carga_id}/ejecutar")
def ejecutar(carga_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Ejecuta la carga del archivo en el servidor SQL Server configurado."""
    carga = db.query(Carga).filter(Carga.id == carga_id).first()
    if not carga:
        raise HTTPException(status_code=404, detail="Carga no encontrada")
    resultado = ejecutar_carga(carga, file)
    return resultado


@router.delete("/{carga_id}", status_code=204)
def eliminar_carga(carga_id: int, db: Session = Depends(get_db)):
    carga = db.query(Carga).filter(Carga.id == carga_id).first()
    if not carga:
        raise HTTPException(status_code=404, detail="Carga no encontrada")
    db.delete(carga)
    db.commit()
