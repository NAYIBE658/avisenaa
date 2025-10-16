from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional, Dict, Any
import logging

from app.schemas.stock import StockCreate, StockUpdate, StockOut

logger = logging.getLogger(__name__)

# --- Funciones CRUD ---

def create_stock(db: Session, stock: StockCreate) -> Optional[int]:
    """Crea un nuevo registro en la tabla stock."""
    try:
        sentencia = text("""
            INSERT INTO stock (
                id_produccion, unidad_medida, cantidad_disponible
            ) VALUES (
                :id_produccion, :unidad_medida, :cantidad_disponible
            )
        """)
        
        result = db.execute(sentencia, stock.model_dump())
        db.commit()
        return result.lastrowid
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear stock: {e}")
        raise Exception("Error de base de datos al crear el registro de stock")

def get_stock_query(db: Session, where_clause: str = "", params: Optional[Dict[str, Any]] = None) -> List[StockOut]:
    """Consulta base para obtener stock con detalles de huevo/producción."""
    query = f"""
        SELECT 
            s.id_producto, s.id_produccion, s.unidad_medida, s.cantidad_disponible,
            ph.fecha, ph.cantidad AS cantidad_producida,
            th.Color, th.Tamaño
        FROM 
            stock s
        INNER JOIN 
            produccion_huevos ph ON s.id_produccion = ph.id_produccion
        INNER JOIN
            tipo_huevos th ON ph.id_tipo_huevo = th.id_tipo_huevo
        {where_clause}
    """
    try:
        results = db.execute(text(query), params).mappings().all()
        return [StockOut.model_validate(dict(result)) for result in results]
    except Exception as e:
        logger.error(f"Error al ejecutar consulta de stock: {e}")
        raise Exception("Error de base de datos al obtener el stock")

def get_stock_by_id(db: Session, stock_id: int) -> Optional[StockOut]:
    """Obtiene un registro de stock por su ID con todos sus detalles."""
    results = get_stock_query(db, "WHERE s.id_producto = :stock_id", {"stock_id": stock_id})
    return results[0] if results else None

def get_all_stock(db: Session) -> List[StockOut]:
    """Obtiene todos los registros de stock con sus detalles."""
    return get_stock_query(db)

def update_stock(db: Session, stock_id: int, stock_update: StockUpdate) -> bool:
    """Actualiza los campos disponibles de un registro de stock."""
    try:
        stock_data = stock_update.model_dump(exclude_unset=True)
        if not stock_data:
            return False

        set_clauses = ", ".join([f"{key} = :{key}" for key in stock_data.keys()])
        sentencia = text(f"""
            UPDATE stock 
            SET {set_clauses}
            WHERE id_producto = :id_producto
        """)

        stock_data["id_producto"] = stock_id

        result = db.execute(sentencia, stock_data)
        db.commit()

        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar stock {stock_id}: {e}")
        raise Exception("Error de base de datos al actualizar el stock")

def delete_stock_by_id(db: Session, stock_id: int) -> bool:
    """Elimina un registro de stock por su ID."""
    try:
        sentencia = text("DELETE FROM stock WHERE id_producto = :id")
        result = db.execute(sentencia, {"id": stock_id})
        db.commit()
        
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar stock {stock_id}: {e}")
        raise Exception("Error de base de datos. El stock puede tener ventas asociadas y no puede ser eliminado.")