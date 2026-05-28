import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.models import DataEntry
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import Usuario
from app.schemas.schemas import DataEntryCreate, DataEntryOut
from app.services.data_entry_service import (
    test_data_entry_config,
    guardar_data_entry,
    ejecutar_data_entry,
    cargar_archivo_existente
)


router = APIRouter()


@router.post("/test")
def test_carga(
    data: DataEntryCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ok, mensaje = test_data_entry_config(
        db=db,
        data=data,
        usuario_id=current_user.id
    )

    if not ok:
        raise HTTPException(status_code=400, detail=mensaje)

    return {
        "exitoso": True,
        "mensaje": mensaje
    }


@router.post("/", response_model=DataEntryOut, status_code=201)
def guardar_carga(
    data: DataEntryCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        return guardar_data_entry(
            db=db,
            data=data,
            usuario_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute")
async def ejecutar_carga(
    metadata: str = Form(...),
    archivo: UploadFile = File(...),
    data_entry_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        data_dict = json.loads(metadata)
        data = DataEntryCreate(**data_dict)

        resultado = await ejecutar_data_entry(
            db=db,
            data=data,
            archivo=archivo,
            usuario_id=current_user.id,
            data_entry_id=data_entry_id
        )

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/by-servidor/{servidor_id}", response_model=List[DataEntryOut])
def listar_data_entries_por_servidor(
    servidor_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(DataEntry).filter(
        DataEntry.usuario_id == current_user.id,
        DataEntry.servidor_id == servidor_id,
        DataEntry.activo == True
    ).all()

@router.post("/{data_entry_id}/load-file")
async def cargar_archivo_data_entry(
    data_entry_id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        resultado = await cargar_archivo_existente(
            db=db,
            data_entry_id=data_entry_id,
            archivo=archivo,
            usuario_id=current_user.id
        )

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )