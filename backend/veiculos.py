from fastapi import APIRouter
from pydantic import BaseModel

from .database import banco
from .usuarios import usuario_e_administrador

router = APIRouter()


class Veiculo(BaseModel):
    id: int
    quantidade: int


@router.get("/api/veiculos")
def listar_veiculos():
    linhas = banco.execute(
        "SELECT id, nome, quantidade FROM veiculos ORDER BY id"
    ).fetchall()
    return [
        {"id": v_id, "nome": nome, "quantidade": quantidade}
        for v_id, nome, quantidade in linhas
    ]


@router.post("/api/veiculos")
def atualizar_veiculos(veiculos: list[Veiculo], id_solicitante: int = 0):
    if not usuario_e_administrador(id_solicitante):
        return {
            "mensagem": "Acesso negado: apenas administradores podem alterar o estoque.",
            "ok": False,
        }

    for veiculo in veiculos:
        banco.execute(
            "UPDATE veiculos SET quantidade = ? WHERE id = ?",
            (veiculo.quantidade, veiculo.id),
        )
    banco.commit()
    return {"mensagem": "Estoque atualizado com sucesso!", "ok": True}