from pydantic import BaseModel, Field
from typing import Optional

class FincaBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    longitud: float
    latitud: float
    id_usuario: int
    estado: bool

class FincaCreate(FincaBase):
    pass

class FincaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=100)
    longitud: Optional[float] = None
    latitud: Optional[float] = None
    id_usuario: Optional[int] = None
    estado: Optional[bool] = None

class FincaOut(FincaBase):
    id_finca: int
