import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend import arsenal, auth, missoes, paginas, usuarios, veiculos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cada módulo do backend tem seu próprio roteador
app.include_router(paginas.router)
app.include_router(auth.router)
app.include_router(arsenal.router)
app.include_router(veiculos.router)
app.include_router(missoes.router)
app.include_router(usuarios.router)

# Arquivos JavaScript da interface
BASE = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE, "frontend")),
    name="frontend",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
