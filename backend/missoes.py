from fastapi import APIRouter
from pydantic import BaseModel

from .database import banco
from .usuarios import usuario_e_administrador

router = APIRouter()


class Missao(BaseModel):
    id: int
    concluida: bool


@router.get("/api/missoes")
def listar_missoes():
    linhas = banco.execute(
        "SELECT id, nome, concluida FROM missoes ORDER BY id"
    ).fetchall()
    return [
        {"id": m_id, "nome": nome, "concluida": bool(concluida)}
        for m_id, nome, concluida in linhas
    ]


@router.post("/api/missoes")
def atualizar_missoes(missoes: list[Missao], id_solicitante: int = 0):
    if not usuario_e_administrador(id_solicitante):
        return {
            "mensagem": "Acesso negado: apenas administradores podem marcar missões como concluídas.",
            "ok": False,
        }

    for missao in missoes:
        banco.execute(
            "UPDATE missoes SET concluida = ? WHERE id = ?",
            (int(missao.concluida), missao.id),
        )
    banco.commit()
    return {"mensagem": "Missões atualizadas com sucesso!", "ok": True}