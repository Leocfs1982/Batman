from fastapi import APIRouter
from pydantic import BaseModel

from .database import banco

router = APIRouter()


class Usuario(BaseModel):
    nome: str
    email: str
    senha: str
    role: str = "usuario"


class DadosLogin(BaseModel):
    email: str
    senha: str


@router.post("/cadastro")
def cadastrar_usuario(usuario: Usuario):
    email_existente = banco.execute(
        "SELECT id FROM usuarios WHERE email = ?", (usuario.email,)
    ).fetchone()

    if email_existente:
        return {
            "mensagem": "Este email já está cadastrado. Não é possível criar outra conta.",
            "ok": False,
        }

    banco.execute(
        "INSERT INTO usuarios (nome, email, senha, role) VALUES (?, ?, ?, ?)",
        (usuario.nome, usuario.email, usuario.senha, usuario.role),
    )
    banco.commit()
    return {"mensagem": "Cadastro salvo no banco de dados!", "ok": True}


@router.post("/login")
def fazer_login(credenciais: DadosLogin):
    usuario = banco.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (credenciais.email, credenciais.senha),
    ).fetchone()

    if usuario:
        return {
            "mensagem": "Entrada realizada com sucesso!",
            "ok": True,
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2],
            "role": usuario[4],
        }
    return {"mensagem": "Email ou senha inválidos!", "ok": False}
