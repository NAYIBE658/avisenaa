from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from app.schemas.fincas import FincaCreate, FincaUpdate, FincaOut
from app.schemas.users import UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import fincas as crud_fincas

router = APIRouter()
modulo = 3  # id_modulo de fincas en la tabla modulos


# Crear finca
@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_finca(
    finca: FincaCreate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        crud_fincas.create_finca(db, finca)
        return {"message": "Finca creada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener finca por ID
@router.get("/by-id/{finca_id}", response_model=FincaOut)
def get_finca(
    finca_id: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        finca = crud_fincas.get_finca_by_id(db, finca_id)
        if not finca:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        return finca

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener todas las fincas
@router.get("/all-fincas", response_model=list[FincaOut])
def get_fincas(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")
        fincas = crud_fincas.get_all_fincas(db)
        return fincas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Actualizar finca por ID
@router.put("/by-id/{finca_id}")
def update_finca(
    finca_id: int,
    finca: FincaUpdate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        success = crud_fincas.update_finca_by_id(db, finca_id, finca)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la finca")

        return {"message": "Finca actualizada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Eliminar finca
@router.delete("/by-id/{finca_id}")
def delete_finca(
    finca_id: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "borrar"):
            raise HTTPException(status_code=401, detail="Usuario no Autorizado")

        success = crud_fincas.delete_finca(db, finca_id)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo eliminar la finca")

        return {"message": "Finca eliminada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))