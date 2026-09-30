import os
import sqlite3

# O banco fica na raiz do projeto.
BASE = os.path.dirname(os.path.dirname(__file__))
CAMINHO_BANCO = os.path.join(BASE, "banco.db")

# A conexão é compartilhada pelos módulos da API.
banco = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)


def inserir_dados_iniciais():
    if banco.execute("SELECT COUNT(*) FROM ferramentas").fetchone()[0] == 0:
        ferramentas = [
            "Bumerangue Metálico",
            "Arma de Gancho (Bat-Garra)",
            "Granadas de Fumaça",
            "Rastreadores",
            "Máscara de Gás e Respirador",
            "Sequenciador Criptográfico",
        ]
        for nome in ferramentas:
            banco.execute(
                "INSERT INTO ferramentas (nome, quantidade) VALUES (?, ?)",
                (nome, 0),
            )
        print("Ferramentas iniciais inseridas no estoque!")

    if banco.execute("SELECT COUNT(*) FROM veiculos").fetchone()[0] == 0:
        veiculos = ["Batmobile", "Batplane", "Batglider", "Batboat", "Batsub"]
        for nome in veiculos:
            banco.execute(
                "INSERT INTO veiculos (nome, quantidade) VALUES (?, ?)",
                (nome, 0),
            )
        print("Veículos iniciais inseridos no estoque!")

    if banco.execute("SELECT COUNT(*) FROM missoes").fetchone()[0] == 0:
        missoes = [
            "Operação Sombrio — Investigar uma série de apagões misteriosos em Gotham.",
            "Código do Morcego — Impedir que um grupo criminoso invada o sistema de segurança da cidade.",
            "Noite de Caça — Rastrear criminosos que estão atacando veículos blindados.",
            "Alerta Arkham — Conter uma fuga em massa no Asilo Arkham.",
            "Operação Submersa — Investigar atividades suspeitas nos túneis subterrâneos de Gotham.",
            "Sombra no Porto — Interceptar um carregamento ilegal chegando ao porto.",
            "Queda do Coringa — Localizar uma série de dispositivos deixados pelo Coringa pela cidade.",
            "Gotham em Chamas — Evacuar uma região da cidade após incêndios criminosos simultâneos.",
            "Rastros na Névoa — Encontrar um informante desaparecido antes que os criminosos o localizem.",
            "Último Sinal — Investigar o desaparecimento de agentes da polícia após perderem comunicação.",
        ]
        for nome in missoes:
            banco.execute(
                "INSERT INTO missoes (nome, concluida) VALUES (?, 0)",
                (nome,),
            )
        print("Missões iniciais inseridas!")


def inicializar_banco():
    banco.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            senha TEXT,
            role TEXT DEFAULT 'usuario'
        )
    """)

    # Mantém bancos antigos funcionando caso a coluna ainda não exista.
    try:
        banco.execute("ALTER TABLE usuarios ADD COLUMN role TEXT DEFAULT 'usuario'")
    except sqlite3.OperationalError:
        pass

    banco.execute("UPDATE usuarios SET role = 'usuario' WHERE role IS NULL OR role = ''")

    if banco.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] == 0:
        banco.execute(
            "INSERT INTO usuarios (nome, email, senha, role) VALUES (?, ?, ?, ?)",
            ("Batman", "batman@gmail.com", "bat123", "admin"),
        )
        print("Usuário Batman criado como administrador: batman@gmail.com")

    banco.execute("""
        CREATE TABLE IF NOT EXISTS ferramentas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER
        )
    """)
    banco.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER
        )
    """)
    banco.execute("""
        CREATE TABLE IF NOT EXISTS missoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            concluida INTEGER DEFAULT 0
        )
    """)

    banco.commit()
    inserir_dados_iniciais()
    banco.commit()


inicializar_banco()
