from pydantic import BaseModel, Field
from typing import Optional

class TipoHuevoBase(BaseModel):
    color: str = Field(min_length=1, max_length=30)
    tamaño: str = Field(min_length=1, max_length=30)

class TipoHuevoCreate(TipoHuevoBase):
    pass

class TipoHuevoUpdate(BaseModel):
    color: Optional[str] = Field(default=None, min_length=1, max_length=30)
    tamaño: Optional[str] = Field(default=None, min_length=1, max_length=30)

class TipoHuevoOut(TipoHuevoBase):
    id_tipo_huevo: int
