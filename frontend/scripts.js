// Quando a página é aberta pelo FastAPI, usamos caminhos relativos.
const API = window.location.port === "8000" ? "" : "http://localhost:8000";

function mostrarFormulario(tipo) {
    document.getElementById("formCadastro").hidden = tipo !== "cadastro";
    document.getElementById("formLogin").hidden = tipo !== "login";
}

document.getElementById("formCadastro").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("emailCad").value,
        senha: document.getElementById("senhaCad").value
    };

    const resposta = await fetch(API + "/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });
    const resultado = await resposta.json();
    alert(resultado.mensagem);

    if (resultado.ok) {
        // Depois de cadastrar, volta para o login para o usuário entrar.
        mostrarFormulario("login");
    }
});

document.getElementById("formLogin").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        email: document.getElementById("emailLogin").value,
        senha: document.getElementById("senhaLogin").value
    };

    const resposta = await fetch(API + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });
    const resultado = await resposta.json();

    if (resultado.ok) {
        // A tela de usuários usa esses dados para verificar o administrador.
        localStorage.setItem("usuario_logado", JSON.stringify(resultado));
        window.location.href = "/arsenal";
    } else {
        alert(resultado.mensagem);
    }
});
