from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProduccionBase(BaseModel):
    """Esquema base para la tabla produccion_huevos."""
    id_galpon: int = Field(..., gt=0, description="ID del galpón donde se registró la producción.")
    cantidad: int = Field(..., gt=0, description="Cantidad de huevos producidos (unidades).")
    fecha: date = Field(..., description="Fecha en que se registró la producción.")
    id_tipo_huevo: int = Field(..., gt=0, description="ID del tipo de huevo (color y tamaño).")

class ProduccionCreate(ProduccionBase):
    """Esquema para crear un nuevo registro de producción."""
    pass

class ProduccionUpdate(BaseModel):
    """Esquema para actualizar un registro de producción. Todos los campos son opcionales."""
    id_galpon: Optional[int] = Field(default=None, gt=0)
    cantidad: Optional[int] = Field(default=None, gt=0)
    fecha: Optional[date] = None
    id_tipo_huevo: Optional[int] = Field(default=None, gt=0)

class ProduccionOut(BaseModel):
    """
    Esquema para mostrar la información detallada de una producción,
    incluyendo datos de galpón y tipo de huevo.
    """
    id_produccion: int
    cantidad: int
    fecha: date
    
    # Datos del Galpón
    id_galpon: int
    nombre_galpon: str = Field(alias="nombre_galpon")
    
    # Datos del Tipo de Huevo
    id_tipo_huevo: int
    color_huevo: str = Field(alias="Color")
    tamano_huevo: str = Field(alias="Tamaño")

    class Config:
        """Permite que el modelo se inicialice a partir de atributos de SQLAlchemy (mapeos)."""
        from_attributes = True
        populate_by_name = True
