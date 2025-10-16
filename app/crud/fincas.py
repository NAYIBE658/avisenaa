from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.fincas import FincaCreate, FincaUpdate

logger = logging.getLogger(__name__)

# Crear finca
def create_finca(db: Session, finca: FincaCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO fincas (
                nombre, longitud, latitud, id_usuario, estado
            ) VALUES (
                :nombre, :longitud, :latitud, :id_usuario, :estado
            )
        """)
        db.execute(sentencia, finca.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear finca: {e}")
        raise Exception("Error de base de datos al crear la finca")

# Obtener finca por ID
def get_finca_by_id(db: Session, id: int):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud, id_usuario, estado
            FROM fincas
            WHERE id_finca = :id_finca
        """)
        result = db.execute(query, {"id_finca": id}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener finca por ID: {e}")
        raise Exception("Error de base de datos al obtener la finca")

# Obtener todas las fincas
def get_all_fincas(db: Session):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud, id_usuario, estado
            FROM fincas
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener fincas: {e}")
        raise Exception("Error de base de datos al obtener las fincas")


# Actualizar finca
def update_finca_by_id(db: Session, finca_id: int, finca: FincaUpdate) -> Optional[bool]:
    try:
        fields = finca.model_dump(exclude_unset=True)
        if not fields:
            return False  # nada que actualizar

        set_clauses = ", ".join([f"{key} = :{key}" for key in fields.keys()])
        sentencia = text(f"""
            UPDATE fincas 
            SET {set_clauses}
            WHERE id_finca = :id_finca
        """)

        fields["id_finca"] = finca_id
        result = db.execute(sentencia, fields)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar finca {finca_id}: {e}")
        raise Exception("Error de base de datos al actualizar la finca")

# Eliminar finca
def delete_finca(db: Session, finca_id: int) -> bool:
    try:
        query = text("DELETE FROM fincas WHERE id_finca = :id_finca")
        result = db.execute(query, {"id_finca": finca_id})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar finca {finca_id}: {e}")
        raise Exception("Error de base de datos al eliminar la finca")