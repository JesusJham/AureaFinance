from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(Integer, primary_key=True, index=True)
    nombres    = Column(String(100), nullable=False)
    apellidos  = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, index=True, nullable=False)
    username   = Column(String(80),  unique=True, index=True, nullable=False)
    password   = Column(String(255), nullable=False)
    activo     = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    servidores = relationship("Servidor", back_populates="usuario")
    cargas     = relationship("Carga", back_populates="usuario")


class Servidor(Base):
    __tablename__ = "servidores"

    id                = Column(Integer, primary_key=True, index=True)
    usuario_id        = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    nombre_servidor   = Column(String(150), nullable=False)
    tipo_bd           = Column(String(50), default="postgresql")
    host              = Column(String(255), nullable=False)
    puerto            = Column(Integer, default=5432)
    name_bd           = Column(String(150), nullable=False)
    user_bd           = Column(String(150), nullable=False)
    pass_bd           = Column(String(255), nullable=False)
    ssl_mode          = Column(String(20), default="require")
    activo            = Column(Boolean, default=True)
    created_at        = Column(DateTime, default=func.now())
    usuario = relationship("Usuario", back_populates="servidores")
    cargas  = relationship("Carga", back_populates="servidor")


class Carga(Base):
    __tablename__ = "cargas"

    id              = Column(Integer, primary_key=True, index=True)
    nombre_tabla    = Column(String(200), nullable=False)
    esquema         = Column(String(100))
    tipo_carga      = Column(String(50))   # INSERT / UPSERT / TRUNCATE+INSERT
    tipo_separador  = Column(String(10))
    codificacion    = Column(String(20), default="UTF-8")
    char_texto      = Column(String(5))
    escape_texto    = Column(String(5))
    mapping_json    = Column(Text)          # JSON con mapeo de columnas
    estado          = Column(String(30), default="pendiente")
    created_at      = Column(DateTime, default=datetime.utcnow)
    executed_at     = Column(DateTime, nullable=True)

    servidor_id = Column(Integer, ForeignKey("servidores.id"))
    servidor    = relationship("Servidor", back_populates="cargas")

    usuario_id  = Column(Integer, ForeignKey("usuarios.id"))
    usuario     = relationship("Usuario", back_populates="cargas")

    
class DataEntry(Base):
    __tablename__ = "data_entries"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    servidor_id = Column(Integer, ForeignKey("servidores.id"))

    nombre_tabla_raw = Column(String(150), nullable=False)
    nombre_tabla_silver = Column(String(150), nullable=False)

    esquema_raw = Column(String(100), default="raw")
    esquema_silver = Column(String(100), default="silver")

    tipo_archivo = Column(String(20), nullable=False)
    encoding = Column(String(50), default="UTF-8")
    separador = Column(String(10))

    tipo_carga = Column(String(30), nullable=False)

    columna_periodo = Column(String(100))
    columna_fecha = Column(String(100))
    columna_delete = Column(String(100))

    truncate_before_load = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    columnas = relationship("DataEntryColumn", back_populates="data_entry")


class DataEntryColumn(Base):
    __tablename__ = "data_entry_columns"

    id = Column(Integer, primary_key=True, index=True)

    data_entry_id = Column(Integer, ForeignKey("data_entries.id"))

    columna_origen = Column(String(200), nullable=False)
    columna_limpia = Column(String(200), nullable=False)

    tipo_origen = Column(String(100))
    tipo_destino = Column(String(100), nullable=False)

    permite_nulos = Column(Boolean, default=True)
    es_primary_key = Column(Boolean, default=False)

    orden = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    data_entry = relationship("DataEntry", back_populates="columnas")