from fastapi import APIRouter, HTTPException
from model.login_seguridad import LoginSeguridadCreate, LoginSeguridadUpdate, LoginSeguridadInDB, LoginSeguridad
from db import database
import random

router = APIRouter()

@router.post("/login/", response_model=LoginSeguridadInDB)
async def crear_login(login: LoginSeguridadCreate):
    # Generar un ID aleatorio para el login
    id_login = random.randint(1, 1000000)
    query = LoginSeguridad.insert().values(
        id_login=id_login,
        **login.dict()
    )
    try:
        await database.execute(query)
        return await database.fetch_one(LoginSeguridad.select().where(LoginSeguridad.c.id_login == id_login))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el login: {str(e)}")

# 5. Modificar el servicio de loginseguridad para que devuelva los usuarios que ingresaron del 1 d enoviembre de 2024 a la fecha de hoy 
@router.get("/login/usuarios_ingresaron/", response_model=list[LoginSeguridadInDB])
async def leer_usuarios_ingresaron():
    query = LoginSeguridad.select().where(LoginSeguridad.c.fecha_ingreso >= '2024-11-01')
    logins = await database.fetch_all(query)
    return logins

@router.get("/login/{login_id}", response_model=LoginSeguridadInDB)
async def leer_login(login_id: int):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    login = await database.fetch_one(query)
    if login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    return login

@router.get("/login/", response_model=list[LoginSeguridadInDB])
async def leer_logins():
    query = LoginSeguridad.select()
    logins = await database.fetch_all(query)
    return logins

@router.put("/login/{login_id}", response_model=LoginSeguridadInDB)
async def actualizar_login(login_id: int, login: LoginSeguridadUpdate):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    db_login = await database.fetch_one(query)
    if db_login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    update_query = LoginSeguridad.update().where(LoginSeguridad.c.id_login == login_id).values(**login.dict())
    await database.execute(update_query)
    return await database.fetch_one(LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id))

@router.delete("/login/{login_id}")
async def eliminar_login(login_id: int):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    db_login = await database.fetch_one(query)
    if db_login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    delete_query = LoginSeguridad.delete().where(LoginSeguridad.c.id_login == login_id)
    await database.execute(delete_query)
    return {"detail": "Login eliminado"}
