from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
import logging

from app.schemas.produccion import ProduccionCreate, ProduccionUpdate

logger = logging.getLogger(__name__)

# --- Consultas de Lectura (GET) ---

def _get_produccion_full_query() -> str:
    """
    Retorna la sentencia SQL base para obtener la producción
    con datos relacionados del galpón y el tipo de huevo.
    """
    return """
        SELECT
            ph.id_produccion, ph.id_galpon, ph.cantidad, ph.fecha, ph.id_tipo_huevo,
            g.nombre AS nombre_galpon,
            th.Color, th.Tamaño
        FROM produccion_huevos ph
        JOIN galpones g ON ph.id_galpon = g.id_galpon
        JOIN tipo_huevos th ON ph.id_tipo_huevo = th.id_tipo_huevo
    """

def get_produccion_by_id(db: Session, produccion_id: int):
    """Obtiene un registro de producción por su ID con datos relacionados."""
    try:
        query = text(f"{_get_produccion_full_query()} WHERE ph.id_produccion = :id_produccion")
        result = db.execute(query, {"id_produccion": produccion_id}).mappings().first()
        return result
    except Exception as e:
        logger.error(f"Error al obtener producción por ID {produccion_id}: {e}")
        raise Exception("Error de base de datos al obtener el registro de producción")

def get_all_produccion(db: Session) -> List:
    """Obtiene todos los registros de producción con sus datos relacionados."""
    try:
        query = text(f"{_get_produccion_full_query()} ORDER BY ph.fecha DESC")
        results = db.execute(query).mappings().all()
        return results
    except Exception as e:
        logger.error(f"Error al obtener todos los registros de producción: {e}")
        raise Exception("Error de base de datos al obtener los registros de producción")

# --- Operación de Creación (POST) ---

def create_produccion(db: Session, produccion: ProduccionCreate) -> Optional[bool]:
    """Crea un nuevo registro de producción de huevos."""
    try:
        sentencia = text("""
            INSERT INTO produccion_huevos (id_galpon, cantidad, fecha, id_tipo_huevo)
            VALUES (:id_galpon, :cantidad, :fecha, :id_tipo_huevo)
        """)
        
        db.execute(sentencia, produccion.model_dump())
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear registro de producción: {e}")
        # En una aplicación real, se podría verificar si el error es por FK (galpón o tipo_huevo inexistente)
        raise Exception("Error de base de datos al crear el registro de producción")

# --- Operación de Actualización (PUT) ---

def update_produccion_by_id(db: Session, produccion_id: int, produccion_update: ProduccionUpdate) -> Optional[bool]:
    """Actualiza la información de un registro de producción por su ID."""
    try:
        produccion_data = produccion_update.model_dump(exclude_unset=True)
        if not produccion_data:
            return False # Nada que actualizar

        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in produccion_data.keys()])
        sentencia = text(f"""
            UPDATE produccion_huevos
            SET {set_clauses}
            WHERE id_produccion = :id_produccion
        """)

        # Agregar el id_produccion
        produccion_data["id_produccion"] = produccion_id

        result = db.execute(sentencia, produccion_data)
        db.commit()

        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar producción {produccion_id}: {e}")
        raise Exception("Error de base de datos al actualizar el registro de producción")

# --- Operación de Borrado (DELETE) ---

def delete_produccion_by_id(db: Session, produccion_id: int) -> Optional[bool]:
    """Elimina un registro de producción por su ID."""
    try:
        sentencia = text("DELETE FROM produccion_huevos WHERE id_produccion = :id_produccion")
        result = db.execute(sentencia, {"id_produccion": produccion_id})
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar producción {produccion_id}: {e}")
        # Manejar el error si hay registros en 'stock' asociados (Foreign Key constraint)
        raise Exception("Error de base de datos al eliminar el registro de producción. Podría estar asociado a un Stock existente.")
