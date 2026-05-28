from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, List
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
    nombre_servidor: str
    tipo_bd: str = "postgresql"
    host: str
    puerto: int = 5432
    name_bd: str
    user_bd: str
    pass_bd: str
    ssl_mode: str = "require"


class ServidorUpdate(BaseModel):
    nombre: Optional[str] = None
    host: Optional[str] = None
    name_bd: Optional[str] = None
    user_bd: Optional[str] = None
    pass_bd: Optional[str] = None


class ServidorOut(BaseModel):
    id: int
    nombre_servidor: str
    tipo_bd: str
    host: str
    puerto: int
    name_bd: str
    user_bd: str
    ssl_mode: str
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


class DataEntryColumnCreate(BaseModel):

    columna_origen: str
    columna_limpia: str
    tipo_origen: Optional[str] = None
    tipo_destino: str
    permite_nulos: bool = True
    es_primary_key: bool = False
    orden: int


class DataEntryColumnOut(DataEntryColumnCreate):

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# DATA ENTRIES
# =========================

class DataEntryCreate(BaseModel):

    servidor_id: int
    nombre_tabla_raw: str
    nombre_tabla_silver: str
    esquema_raw: str = "raw"
    esquema_silver: str = "silver"
    tipo_archivo: str
    encoding: str = "UTF-8"
    separador: Optional[str] = None
    tipo_carga: str
    columna_periodo: Optional[str] = None
    columna_fecha: Optional[str] = None
    columna_delete: Optional[str] = None
    columnas: List[DataEntryColumnCreate]


class DataEntryOut(BaseModel):

    id: int
    usuario_id: int
    servidor_id: int
    nombre_tabla_raw: str
    nombre_tabla_silver: str
    esquema_raw: str
    esquema_silver: str
    tipo_archivo: str
    encoding: str
    separador: Optional[str]
    tipo_carga: str
    columna_periodo: Optional[str]
    columna_fecha: Optional[str]
    columna_delete: Optional[str]
    truncate_before_load: bool
    activo: bool
    created_at: datetime
    columnas: List[DataEntryColumnOut] = []

    class Config:
        from_attributes = True