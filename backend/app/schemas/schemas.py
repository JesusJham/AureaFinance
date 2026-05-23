from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    username: str
    password: str


class UsuarioOut(BaseModel):
    id: int
    nombres: str
    apellidos: str
    email: str
    username: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


# ── Servidor ──────────────────────────────────────────────────────────────────

class ServidorCreate(BaseModel):
    nombre: str
    host: str
    name_bd: str
    user_bd: str
    pass_bd: str


class ServidorUpdate(BaseModel):
    nombre: Optional[str] = None
    host: Optional[str] = None
    name_bd: Optional[str] = None
    user_bd: Optional[str] = None
    pass_bd: Optional[str] = None


class ServidorOut(BaseModel):
    id: int
    nombre: str
    host: str
    name_bd: str
    user_bd: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Carga ─────────────────────────────────────────────────────────────────────

class CargaCreate(BaseModel):
    servidor_id: int
    nombre_tabla: str
    esquema: Optional[str] = None
    tipo_carga: Optional[str] = "INSERT"
    tipo_separador: Optional[str] = ","
    codificacion: Optional[str] = "UTF-8"
    char_texto: Optional[str] = None
    escape_texto: Optional[str] = None
    mapping_json: Optional[str] = None


class CargaOut(BaseModel):
    id: int
    nombre_tabla: str
    esquema: Optional[str]
    tipo_carga: Optional[str]
    estado: str
    created_at: datetime
    executed_at: Optional[datetime]

    class Config:
        from_attributes = True
