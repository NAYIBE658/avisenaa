from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import users
from app.router import auth
from app.router import fincas 
from app.router import tipo_huevos
from app.router import produccion
from app.router import stock

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(fincas.router, prefix="/fincas", tags=["fincas"]) 
app.include_router(produccion.router, prefix="/produccion", tags=["produccion"]) 
app.include_router(stock.router, prefix="/stock", tags=["stock"]) 
app.include_router(tipo_huevos.router, prefix="/tipo_huevos", tags=["tipo_huevos"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
        "message": "ok",
        "autor": "ADSO 2925889"
    }

