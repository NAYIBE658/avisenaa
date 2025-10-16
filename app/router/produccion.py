from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importar dependencias
from core.database import get_db
from app.schemas.produccion import ProduccionCreate, ProduccionOut, ProduccionUpdate
from app.crud import produccion as crud_produccion
# from app.router.dependencies import get_current_user # Asumimos que la autenticación se implementaría aquí

router = APIRouter(
    prefix="/produccion",
    tags=["Producción de Huevos"],
    # dependencies=[Depends(get_current_user)] # Descomentar cuando la autenticación esté lista
)

@router.post("/crear", response_model=None, status_code=status.HTTP_201_CREATED)
def create_produccion_record(produccion: ProduccionCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva producción de huevos en un galpón y tipo de huevo específicos.
    """
    try:
        crud_produccion.create_produccion(db, produccion)
        return {"message": "Registro de producción creado correctamente"}
    except Exception as e:
        # Aquí capturamos errores como la violación de FK (si galpón o tipo_huevo no existen)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[ProduccionOut])
def get_all_produccion_records(db: Session = Depends(get_db)):
    """
    Obtiene todos los registros de producción con detalles de galpón y tipo de huevo.
    """
    try:
        records = crud_produccion.get_all_produccion(db)
        if not records:
            return []
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{produccion_id}", response_model=ProduccionOut)
def get_produccion_record_by_id(produccion_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un registro de producción específico por su ID.
    """
    try:
        record = crud_produccion.get_produccion_by_id(db, produccion_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Registro de producción con ID {produccion_id} no encontrado")
        return record
    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{produccion_id}", status_code=status.HTTP_200_OK)
def update_produccion_record(produccion_id: int, produccion: ProduccionUpdate, db: Session = Depends(get_db)):
    """
    Actualiza parcialmente los datos de un registro de producción.
    """
    try:
        success = crud_produccion.update_produccion_by_id(db, produccion_id, produccion)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de producción no encontrado o no se proporcionaron campos para actualizar")
        return {"message": "Registro de producción actualizado correctamente"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{produccion_id}", status_code=status.HTTP_200_OK)
def delete_produccion_record(produccion_id: int, db: Session = Depends(get_db)):
    """
    Elimina un registro de producción por su ID.
    """
    try:
        success = crud_produccion.delete_produccion_by_id(db, produccion_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Registro de producción con ID {produccion_id} no encontrado")
        return {"message": "Registro de producción eliminado correctamente"}
    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e
        # Manejo de error de clave foránea si está en uso por la tabla 'stock'
        if "Foreign Key constraint" in str(e):
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar la producción ya que tiene productos asociados en el stock.")
        raise HTTPException(status_code=500, detail=str(e))
