from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_current_user
from app.models.models import Usuario

from app.core.database import get_db
from app.models.models import Servidor
from app.schemas.schemas import (
    ServidorCreate,
    ServidorUpdate,
    ServidorOut
)
from app.services.servidor_service import test_database_connection
from app.core.deps import get_current_user
from app.models.models import Usuario
from app.services.servidor_service import get_database_schemas


router = APIRouter()


@router.get("/", response_model=List[ServidorOut])
def listar_servidores(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Servidor).filter(
        Servidor.activo == True,
        Servidor.usuario_id == current_user.id
    ).all()


@router.post("/", response_model=ServidorOut, status_code=201)
def crear_servidor(
    data: ServidorCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    servidor = Servidor(
        **data.model_dump(),
        usuario_id=current_user.id
    )

    db.add(servidor)

    db.commit()

    db.refresh(servidor)

    return servidor


@router.post("/test-connection")
def probar_conexion_directa(data: ServidorCreate):

    ok, mensaje = test_database_connection(data)

    if not ok:
        raise HTTPException(
            status_code=400,
            detail=mensaje
        )

    return {
        "exitoso": ok,
        "mensaje": mensaje
    }


@router.get("/{servidor_id}", response_model=ServidorOut)
def obtener_servidor(
    servidor_id: int,
    db: Session = Depends(get_db)
):
    srv = (
        db.query(Servidor)
        .filter(Servidor.id == servidor_id)
        .first()
    )

    if not srv:
        raise HTTPException(
            status_code=404,
            detail="Servidor no encontrado"
        )

    return srv


@router.put("/{servidor_id}", response_model=ServidorOut)
def actualizar_servidor(
    servidor_id: int,
    data: ServidorUpdate,
    db: Session = Depends(get_db)
):
    srv = (
        db.query(Servidor)
        .filter(Servidor.id == servidor_id)
        .first()
    )

    if not srv:
        raise HTTPException(
            status_code=404,
            detail="Servidor no encontrado"
        )

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(srv, field, value)

    db.commit()
    db.refresh(srv)

    return srv


@router.delete("/{servidor_id}", status_code=204)
def eliminar_servidor(
    servidor_id: int,
    db: Session = Depends(get_db)
):
    srv = (
        db.query(Servidor)
        .filter(Servidor.id == servidor_id)
        .first()
    )

    if not srv:
        raise HTTPException(
            status_code=404,
            detail="Servidor no encontrado"
        )

    srv.activo = False

    db.commit()

    return None


@router.post("/{servidor_id}/test")
def probar_conexion_guardada(
    servidor_id: int,
    db: Session = Depends(get_db)
):
    srv = (
        db.query(Servidor)
        .filter(Servidor.id == servidor_id)
        .first()
    )

    if not srv:
        raise HTTPException(
            status_code=404,
            detail="Servidor no encontrado"
        )

    ok, mensaje = test_database_connection(srv)

    if not ok:
        raise HTTPException(
            status_code=400,
            detail=mensaje
        )

    return {
        "exitoso": ok,
        "mensaje": mensaje
    }

@router.get("/{servidor_id}/schemas")
def listar_schemas_servidor(
    servidor_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    srv = db.query(Servidor).filter(
        Servidor.id == servidor_id,
        Servidor.usuario_id == current_user.id
    ).first()

    if not srv:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")

    ok, schemas = get_database_schemas(srv)

    if not ok:
        raise HTTPException(status_code=400, detail=schemas)

    return schemas