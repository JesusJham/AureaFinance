from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioOut, LoginRequest, Token

router = APIRouter()


@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(data: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(
        (Usuario.username == data.username) | (Usuario.email == data.email)
    ).first():
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")

    user = Usuario(
        nombres=data.nombres,
        apellidos=data.apellidos,
        email=data.email,
        username=data.username,
        password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "usuario": user}
