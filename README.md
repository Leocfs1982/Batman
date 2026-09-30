# FullAPI — Sistema da Batcave

Este é um projeto escolar para controlar algumas informações da Batcave. Ele possui cadastro e login de usuários, estoque de ferramentas, estoque de veículos, lista de missões e controle de acesso de administradores.

## Funcionalidades

- Cadastro e entrada de usuários.
- Controle da quantidade de ferramentas do arsenal.
- Controle da quantidade de veículos.
- Lista de missões que podem ser marcadas como concluídas.
- Gerenciamento de usuários para administradores.
- Documentação automática da API em `/docs`.

## Tecnologias utilizadas

- Python com FastAPI no backend.
- SQLite para o banco de dados.
- HTML, CSS e JavaScript no frontend.
- Uvicorn para executar o servidor.

## Como instalar

É necessário ter o Python 3.10 ou uma versão mais recente instalado.

Na pasta do projeto, crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows, use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Depois, instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Com o ambiente virtual ativado, execute:

```bash
python main.py
```

Também é possível executar com recarga automática durante o desenvolvimento:

```bash
uvicorn main:app --reload
```

Abra `http://localhost:8000` no navegador. Não abra os arquivos HTML diretamente pelo gerenciador de arquivos.

## Usuário inicial

Na primeira execução, o sistema cria um administrador:

| Campo | Valor |
|---|---|
| Nome | Batman |
| Email | `batman@gmail.com` |
| Senha | `bat123` |
| Nível de acesso | `admin` |

## Banco de dados

O arquivo `banco.db` é criado automaticamente. Ele guarda os usuários, as ferramentas, os veículos e as missões.

Para começar novamente com os dados iniciais, pare o servidor, apague o arquivo `banco.db` e execute o projeto outra vez. Essa ação apaga os dados cadastrados.

## Organização das pastas

- `main.py`: inicia a aplicação e reúne as rotas.
- `backend/`: contém a API, o banco de dados e as páginas.
- `frontend/`: contém os arquivos JavaScript das telas.
- `templates/`: contém as páginas HTML.
- `requirements.txt`: lista as dependências do projeto.
- `banco.db`: banco de dados criado pelo sistema.
