from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from app.schemas.tipo_huevos import TipoHuevoCreate, TipoHuevoUpdate, TipoHuevoOut
from app.schemas.users import UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import tipo_huevos as crud_tipo_huevo

router = APIRouter()
modulo = 3  # id_modulo de tipo_huevo en la tabla modulos


# Crear tipo_huevo
@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_tipo_huevo(
    tipo_huevo: TipoHuevoCreate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        crud_tipo_huevo.create_tipo_huevo(db, tipo_huevo)
        return {"message": "Tipo de huevo creada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener por ID
@router.get("/by-id/{tipo_id}", response_model=TipoHuevoOut)
def get_tipo_huevo(
    tipo_id: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        tipo_huevo = crud_tipo_huevo.get_tipo_huevo_by_id(db, tipo_id)
        if not tipo_huevo:
            raise HTTPException(status_code=404, detail="Tipo de huevo no encontrada")
        return tipo_huevo

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener todos
@router.get("/all-tipo_huevos", response_model=list[TipoHuevoOut])
def get_all_tipo_huevos(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")
        tipo_huevos = crud_tipo_huevo.get_all_tipo_huevos(db)
        return tipo_huevos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Actualizar por ID
@router.put("/by-id/{tipo_id}")
def update_tipo_huevo(
    tipo_id: int,
    tipo_huevo: TipoHuevoUpdate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        success = crud_tipo_huevo.update_tipo_huevo_by_id(db, tipo_id, tipo_huevo)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el tipo de huevo")

        return {"message": "Tipo de huevo actualizada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Eliminar tipo_huevo
@router.delete("/by-id/{tipo_id}")
def delete_tipo_huevo(
    tipo_id: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "borrar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        success = crud_tipo_huevo.delete_tipo_huevo(db, tipo_id)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo eliminar el tipo de huevo")

        return {"message": "Tipo de huevo eliminado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
