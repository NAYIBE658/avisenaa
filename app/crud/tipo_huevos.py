from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.tipo_huevos import TipoHuevoCreate, TipoHuevoUpdate

logger = logging.getLogger(__name__)

# Crear tipo_huevo
def create_tipo_huevo(db: Session, tipo_huevo: TipoHuevoCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO tipo_huevos (
                Color, Tamaño
            ) VALUES (
                :color, :tamaño
            )
        """)
        db.execute(sentencia, tipo_huevo.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear el tipo de huevo: {e}")
        raise Exception("Error de base de datos al crear el tipo de huevo")

# Obtener tipo_huevo por ID
def get_tipo_huevo_by_id(db: Session, id: int):
    try:
        query = text("""
            SELECT id_tipo_huevo, Color, Tamaño
            FROM tipo_huevos
            WHERE id_tipo_huevo = :id_tipo_huevo
        """)
        result = db.execute(query, {"id_tipo_huevo": id}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener el tipo de huevo por ID: {e}")
        raise Exception("Error de base de datos al obtener el tipo de huevo")

# Obtener todas los tipo_huevos
def get_all_tipo_huevos(db: Session):
    try:
        query = text("""
            SELECT id_tipo_huevo, Color, Tamaño
            FROM tipo_huevos
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener los tipos de huevo: {e}")
        raise Exception("Error de base de datos al obtener los tipos de huevo")

# Actualizar tipo_huevo
def update_tipo_huevo_by_id(db: Session, tipo_id: int, tipo_huevo: TipoHuevoUpdate) -> Optional[bool]:
    try:
        fields = tipo_huevo.model_dump(exclude_unset=True)
        if not fields:
            return False  # nada que actualizar

        set_clauses = ", ".join([f"{key} = :{key}" for key in fields.keys()])
        sentencia = text(f"""
            UPDATE tipo_huevos
            SET {set_clauses}
            WHERE id_tipo_huevo = :id_tipo_huevo
        """)
        fields["id_tipo_huevo"] = tipo_id
        result = db.execute(sentencia, fields)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tipo_huevo {tipo_id}: {e}")
        raise Exception("Error de base de datos al actualizar el tipo de huevo")

# Eliminar tipo_huevo
def delete_tipo_huevo(db: Session, tipo_id: int) -> bool:
    try:
        query = text("DELETE FROM tipo_huevos WHERE id_tipo_huevo = :id_tipo_huevo")
        result = db.execute(query, {"id_tipo_huevo": tipo_id})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar el tipo de huevo {tipo_id}: {e}")
        raise Exception("Error de base de datos al eliminar el tipo de huevo")
