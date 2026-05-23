from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Servidor
from app.schemas.schemas import ServidorCreate, ServidorUpdate, ServidorOut
from app.services.servidor_service import test_sql_server_connection

router = APIRouter()


@router.get("/", response_model=List[ServidorOut])
def listar_servidores(db: Session = Depends(get_db)):
    return db.query(Servidor).filter(Servidor.activo == True).all()


@router.post("/", response_model=ServidorOut, status_code=201)
def crear_servidor(data: ServidorCreate, db: Session = Depends(get_db)):
    servidor = Servidor(**data.model_dump())
    db.add(servidor)
    db.commit()
    db.refresh(servidor)
    return servidor


@router.get("/{servidor_id}", response_model=ServidorOut)
def obtener_servidor(servidor_id: int, db: Session = Depends(get_db)):
    srv = db.query(Servidor).filter(Servidor.id == servidor_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    return srv


@router.put("/{servidor_id}", response_model=ServidorOut)
def actualizar_servidor(servidor_id: int, data: ServidorUpdate, db: Session = Depends(get_db)):
    srv = db.query(Servidor).filter(Servidor.id == servidor_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(srv, field, value)
    db.commit()
    db.refresh(srv)
    return srv


@router.delete("/{servidor_id}", status_code=204)
def eliminar_servidor(servidor_id: int, db: Session = Depends(get_db)):
    srv = db.query(Servidor).filter(Servidor.id == servidor_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    srv.activo = False
    db.commit()


@router.post("/{servidor_id}/test")
def probar_conexion(servidor_id: int, db: Session = Depends(get_db)):
    srv = db.query(Servidor).filter(Servidor.id == servidor_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    ok, mensaje = test_sql_server_connection(srv)
    return {"exitoso": ok, "mensaje": mensaje}
