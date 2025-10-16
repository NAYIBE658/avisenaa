# router_stock.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from app.router.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.stock import StockCreate, StockUpdate, StockOut
from app.crud import stock as crud_stock

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_stock_record(
    stock: StockCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Crea un nuevo registro de producto en el stock."""
    try:
        stock_id = crud_stock.create_stock(db, stock)
        return {"message": "Registro de stock creado correctamente", "id_producto": stock_id}
    except Exception as e:
        # Convertimos error en HTTPException para que FastAPI lo muestre correctamente
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[StockOut])
def get_all_stock_records(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Obtiene todos los registros de stock con sus detalles de producción y tipo de huevo."""
    try:
        stock_list = crud_stock.get_all_stock(db)
        return stock_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_id}", response_model=StockOut)
def get_stock_by_id(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Obtiene un registro de stock específico por ID."""
    try:
        stock_record = crud_stock.get_stock_by_id(db, stock_id)
        if not stock_record:
            raise HTTPException(status_code=404, detail="Registro de stock no encontrado")
        return stock_record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{stock_id}")
def update_stock_record(
    stock_id: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Actualiza campos de un registro de stock (ej. cantidad_disponible o unidad_medida)."""
    try:
        success = crud_stock.update_stock(db, stock_id, stock)
        if not success:
            raise HTTPException(status_code=404, detail="Registro de stock no encontrado o no hay cambios para aplicar")
        return {"message": "Stock actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_record(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Elimina un registro de stock por ID."""
    try:
        success = crud_stock.delete_stock_by_id(db, stock_id)
        if not success:
            raise HTTPException(status_code=404, detail="Registro de stock no encontrado")
        return  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
