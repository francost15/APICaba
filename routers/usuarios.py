from fastapi import APIRouter, HTTPException
from model.usuario import UsuarioCreate, UsuarioUpdate, UsuarioInDB, Usuarios
from db import database
from passlib.context import CryptContext
import random

router = APIRouter()


# Modificar el servicio de Usuarios para que devuelva los que tiene rol de capturista y con estado Activo
# Modificar el servicio de Usuarios para que devuelva los que tiene rol de capturista y con estado Activo
@router.get("/usuarios/roles_capturista/", response_model=list[UsuarioInDB])
async def leer_usuarios_roles_capturista():
    query = Usuarios.select().where(Usuarios.c.rol == 'capturistas').where(Usuarios.c.status == 'activo')
    usuarios = await database.fetch_all(query)
    if usuarios is None:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con rol de capturista y estado activo")
    return usuarios

@router.post("/usuarios/", response_model=UsuarioInDB)
async def crear_usuario(usuario: UsuarioCreate):
    # Generar un ID aleatorio para el usuario
    id_usuario = random.randint(1, 1000000)
    usuario_dict = usuario.dict()
    usuario_dict["id_usuario"] = id_usuario
    usuario_dict["contraseña"] = (usuario_dict["contraseña"])
    query = Usuarios.insert().values(**usuario_dict)
    await database.execute(query)
    return await database.fetch_one(Usuarios.select().where(Usuarios.c.id_usuario == id_usuario))

@router.get("/usuarios/{usuario_id}", response_model=UsuarioInDB)
async def leer_usuario(usuario_id: int):
    query = Usuarios.select().where(Usuarios.c.id_usuario == usuario_id)
    usuario = await database.fetch_one(query)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/usuarios/", response_model=list[UsuarioInDB])
async def leer_usuarios():
    query = Usuarios.select()
    usuarios = await database.fetch_all(query)
    return usuarios

@router.put("/usuarios/{usuario_id}", response_model=UsuarioInDB)
async def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    query = Usuarios.select().where(Usuarios.c.id_usuario == usuario_id)
    db_usuario = await database.fetch_one(query)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = {k: v for k, v in usuario.dict(exclude_unset=True).items()}
    if "contraseña" in update_data:
        update_data["contraseña"] =(update_data["contraseña"])
    update_query = Usuarios.update().where(Usuarios.c.id_usuario == usuario_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(Usuarios.select().where(Usuarios.c.id_usuario == usuario_id))

@router.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: int):
    query = Usuarios.select().where(Usuarios.c.id_usuario == usuario_id)
    db_usuario = await database.fetch_one(query)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    delete_query = Usuarios.delete().where(Usuarios.c.id_usuario == usuario_id)
    await database.execute(delete_query)
    return {"detail": "Usuario eliminado"}
