from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
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

    id         = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    nombre     = Column(String(150), nullable=False)
    host       = Column(String(255), nullable=False)
    name_bd    = Column(String(150), nullable=False)
    user_bd    = Column(String(150), nullable=False)
    pass_bd    = Column(String(255), nullable=False)
    activo     = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


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

    
