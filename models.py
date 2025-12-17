from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass


class TipoEquipamento(enum.Enum):
    NOVO = "NOVO"
    USADO = "USADO"


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin' ou 'usuario'


class Equipment(Base):
    __tablename__ = 'equipments'
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # 'NOVO' ou 'USADO'
    quantidade = Column(Integer, nullable=False, default=0)
    data_adicao = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)

