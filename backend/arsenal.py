from fastapi import APIRouter
from pydantic import BaseModel

from .database import banco
from .usuarios import usuario_e_administrador

router = APIRouter()


class Ferramenta(BaseModel):
    id: int
    quantidade: int


@router.get("/ferramentas")
def listar_ferramentas():
    linhas = banco.execute(
        "SELECT id, nome, quantidade FROM ferramentas ORDER BY id"
    ).fetchall()
    return [
        {"id": f_id, "nome": nome, "quantidade": quantidade}
        for f_id, nome, quantidade in linhas
    ]


@router.post("/ferramentas")
def atualizar_ferramentas(ferramentas: list[Ferramenta], id_solicitante: int = 0):
    if not usuario_e_administrador(id_solicitante):
        return {
            "mensagem": "Acesso negado: apenas administradores podem alterar o estoque.",
            "ok": False,
        }

    for ferramenta in ferramentas:
        banco.execute(
            "UPDATE ferramentas SET quantidade = ? WHERE id = ?",
            (ferramenta.quantidade, ferramenta.id),
        )
    banco.commit()
    return {"mensagem": "Estoque atualizado com sucesso!", "ok": True}