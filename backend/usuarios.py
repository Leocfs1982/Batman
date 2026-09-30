from fastapi import APIRouter
from pydantic import BaseModel

from .database import banco

router = APIRouter()


def usuario_e_administrador(id_usuario: int) -> bool:
    """Verifica se o usuário tem acesso de administrador."""
    if id_usuario <= 0:
        return False

    linha = banco.execute(
        "SELECT role FROM usuarios WHERE id = ?", (id_usuario,)
    ).fetchone()
    return bool(linha and linha[0] == "admin")


class DadosPermissao(BaseModel):
    id: int
    role: str
    id_solicitante: int = 0


@router.get("/api/usuarios")
def listar_usuarios():
    linhas = banco.execute(
        "SELECT id, nome, email, senha, role FROM usuarios ORDER BY id"
    ).fetchall()
    return [
        {"id": id_usuario, "nome": nome, "email": email, "senha": senha, "role": role}
        for id_usuario, nome, email, senha, role in linhas
    ]


@router.post("/api/usuarios/role")
def atualizar_permissao(dados: DadosPermissao):
    if not usuario_e_administrador(dados.id_solicitante):
        return {
            "mensagem": "Acesso negado: apenas um administrador pode alterar níveis de acesso.",
            "ok": False,
        }

    banco.execute(
        "UPDATE usuarios SET role = ? WHERE id = ?",
        (dados.role, dados.id),
    )
    banco.commit()
    return {"mensagem": "Nível de acesso atualizado com sucesso!", "ok": True}


@router.post("/api/usuarios/eliminar")
def excluir_usuario(dados: DadosPermissao):
    if not usuario_e_administrador(dados.id_solicitante):
        return {
            "mensagem": "Acesso negado: apenas um administrador pode excluir usuários.",
            "ok": False,
        }

    banco.execute("DELETE FROM usuarios WHERE id = ?", (dados.id,))
    banco.commit()
    return {"mensagem": "Usuário excluído com sucesso!", "ok": True}
