# schemas_stock.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import date

# Definir el tipo de unidad de medida basado en la base de datos
UnidadMedida = Literal['unidad', 'panal', 'docena', 'medio_panal']


class StockBase(BaseModel):
    """Modelo base para las propiedades de un registro de stock."""
    id_produccion: int = Field(..., ge=1, description="ID de la producción de huevos (FK a produccion_huevos)")
    unidad_medida: UnidadMedida = Field(..., description="Unidad de medida del producto")
    cantidad_disponible: int = Field(..., ge=0, description="Cantidad de producto disponible")


class StockCreate(StockBase):
    """Schema para crear un nuevo registro de stock."""
    pass


class StockUpdate(BaseModel):
    """Schema para actualizar campos del stock. Los campos son opcionales."""
    unidad_medida: Optional[UnidadMedida] = Field(None, description="Nueva unidad de medida")
    cantidad_disponible: Optional[int] = Field(None, ge=0, description="Nueva cantidad de producto disponible")


class StockOut(BaseModel):
    """
    Schema para la respuesta de un registro de stock, incluyendo detalles de producción y huevo.
    Use `alias` si la consulta SQL devuelve un nombre distinto.
    """
    id_producto: int = Field(..., description="ID del registro de stock")
    id_produccion: int
    unidad_medida: str
    cantidad_disponible: int

    # Detalles obtenidos de las tablas JOIN (alias si la consulta los devuelve así)
    fecha_produccion: date = Field(..., alias="fecha")
    cantidad_producida: int = Field(..., alias="cantidad_producida")
    color_huevo: str = Field(..., alias="Color")
    tamano_huevo: str = Field(..., alias="Tamaño")

    class Config:
        from_attributes = True
        populate_by_name = True
