from fastapi import APIRouter, HTTPException
from model.reseñas_productos import ResenaProductoCreate, ResenaProductoUpdate, ResenaProductoInDB, ResenasProducto
from db import database
import random

router = APIRouter()

@router.post("/resenas/", response_model=ResenaProductoInDB)
async def crear_resena(resena: ResenaProductoCreate):
    # Generar un ID aleatorio para la reseña
    id_resena = random.randint(1, 1000000)
    query = ResenasProducto.insert().values(
        id_resena=id_resena,
        id_cliente=resena.id_cliente,
        id_producto=resena.id_producto,
        calificacion=resena.calificacion,
        comentario=resena.comentario,
        status=resena.status,
        empleado_mod=resena.empleado_mod
    )
    try:
        await database.execute(query)
        return await database.fetch_one(ResenasProducto.select().where(ResenasProducto.c.id_resena == id_resena))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la reseña: {str(e)}")

@router.get("/resenas/{resena_id}", response_model=ResenaProductoInDB)
async def leer_resena(resena_id: int):
    query = ResenasProducto.select().where(ResenasProducto.c.id_resena == resena_id)
    resena = await database.fetch_one(query)
    if resena is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return resena

@router.get("/resenas/", response_model=list[ResenaProductoInDB])
async def leer_resenas():
    query = ResenasProducto.select()
    resenas = await database.fetch_all(query)
    return resenas

@router.put("/resenas/{resena_id}", response_model=ResenaProductoInDB)
async def actualizar_resena(resena_id: int, resena: ResenaProductoUpdate):
    query = ResenasProducto.select().where(ResenasProducto.c.id_resena == resena_id)
    db_resena = await database.fetch_one(query)
    if db_resena is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    update_data = {k: v for k, v in resena.dict(exclude_unset=True).items()}
    update_query = ResenasProducto.update().where(ResenasProducto.c.id_resena == resena_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(ResenasProducto.select().where(ResenasProducto.c.id_resena == resena_id))

@router.delete("/resenas/{resena_id}")
async def eliminar_resena(resena_id: int):
    query = ResenasProducto.select().where(ResenasProducto.c.id_resena == resena_id)
    db_resena = await database.fetch_one(query)
    if db_resena is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    delete_query = ResenasProducto.delete().where(ResenasProducto.c.id_resena == resena_id)
    await database.execute(delete_query)
    return {"detail": "Reseña eliminada"}