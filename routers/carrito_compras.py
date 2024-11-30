import random
from fastapi import APIRouter, HTTPException
from model.carrito_compras import CarritoComprasCreate, CarritoComprasUpdate, CarritoComprasInDB, CarritoCompras
from db import database

router = APIRouter()

@router.post("/carritos/", response_model=CarritoComprasInDB)
async def crear_carrito(carrito: CarritoComprasCreate):
    id_carrito = random.randint(1, 1000000)
    query = CarritoCompras.insert().values(
        id_carrito=id_carrito,
        id_cliente=carrito.id_cliente,
        fecha_creacion=carrito.fecha_creacion,
        total=carrito.total,
        estado=carrito.estado,
        status=carrito.status,
        empleado_mod=carrito.empleado_mod
    )
    try:
        await database.execute(query)
        return {**carrito.dict(), "id_carrito": id_carrito}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el carrito: {str(e)}")
# 3. Modificar el servicio de carrito de compras para que devuelva los que el total es mayour a 1000
# 3. Modificar el servicio de carrito de compras para que devuelva los que sus totales sean entre 1000 y 10000
@router.get("/carritos/mayor_mil/", response_model=list[CarritoComprasInDB])
async def leer_carritos_mayor_mil():
    query = CarritoCompras.select().where(CarritoCompras.c.total.between(1000, 10000))
    carritos = await database.fetch_all(query)
    if carritos is None:
        raise HTTPException(status_code=404, detail="No se encontraron carritos con total entre 1000 y 10000")
    return carritos
        
@router.get("/carritos/{carrito_id}", response_model=CarritoComprasInDB)
async def leer_carrito(carrito_id: int):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    carrito = await database.fetch_one(query)
    if carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito

@router.get("/carritos/", response_model=list[CarritoComprasInDB])
async def leer_todos_los_carritos():
    query = CarritoCompras.select()
    carritos = await database.fetch_all(query)
    return carritos

@router.put("/carritos/{carrito_id}", response_model=CarritoComprasInDB)
async def actualizar_carrito(carrito_id: int, carrito: CarritoComprasUpdate):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    db_carrito = await database.fetch_one(query)
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    update_data = {k: v for k, v in carrito.dict(exclude_unset=True).items()}
    update_query = CarritoCompras.update().where(CarritoCompras.c.id_carrito == carrito_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id))

@router.delete("/carritos/{carrito_id}")
async def eliminar_carrito(carrito_id: int):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    db_carrito = await database.fetch_one(query)
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    delete_query = CarritoCompras.delete().where(CarritoCompras.c.id_carrito == carrito_id)
    await database.execute(delete_query)
    return {"detail": "Carrito eliminado"}
