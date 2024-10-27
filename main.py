from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cliente, carrito_compras, detalle_carrito, detalle_pedido, historial_compras, login_seguridad, metodo_pago, reseñas_productos, roles, usuarios, pedidos
from db import connect_db, disconnect_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shop-limpieza.vercel.app", "http://localhost:3000"],  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos
    allow_headers=["*"],  # Headers permitidos
)

@app.on_event("startup")
async def startup():
    await connect_db()
    logger.info("API iniciada y conexión a la base de datos verificada.")

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()
    logger.info("API detenida y conexión a la base de datos cerrada.")

@app.get("/")
async def read_item():
    return {"message": "Bienvenido final"}

app.include_router(cliente.router)
app.include_router(carrito_compras.router)
app.include_router(detalle_carrito.router)
app.include_router(detalle_pedido.router)
app.include_router(historial_compras.router)
app.include_router(login_seguridad.router)
app.include_router(metodo_pago.router)
app.include_router(reseñas_productos.router)
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)