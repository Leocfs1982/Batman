import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
BASE = os.path.dirname(os.path.dirname(__file__))
PASTA_TEMPLATES = os.path.join(BASE, "templates")


def enviar_pagina(nome_arquivo: str):
    """Envia uma página sem permitir que o navegador use uma versão antiga."""
    return FileResponse(
        os.path.join(PASTA_TEMPLATES, nome_arquivo),
        headers={"Cache-Control": "no-store"},
    )


@router.get("/")
def index():
    return enviar_pagina("index.html")


@router.get("/arsenal")
def arsenal():
    return enviar_pagina("arsenal.html")


@router.get("/veiculos")
def veiculos():
    return enviar_pagina("veiculos.html")


@router.get("/missoes")
def missoes():
    return enviar_pagina("missoes.html")


@router.get("/usuarios")
def usuarios():
    return enviar_pagina("usuarios.html")
