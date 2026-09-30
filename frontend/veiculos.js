// A página é aberta diretamente pelo FastAPI (http://localhost:8000/veiculos),
// então usamos caminhos relativos (o frontend e o backend estão juntos).

// Dados do usuário logado salvos na tela de entrada (mesmo padrão da página de usuários).
const usuarioLogado = JSON.parse(localStorage.getItem("usuario_logado") || "null");
const idUsuario = usuarioLogado ? usuarioLogado.id : 0;
const eAdministrador = usuarioLogado && usuarioLogado.role === "admin";

async function carregarEstoque() {
    const resposta = await fetch("/api/veiculos");
    const veiculos = await resposta.json();

    const corpoTabela = document.getElementById("corpoTabela");
    corpoTabela.innerHTML = "";

    for (const veiculo of veiculos) {
        const linha = document.createElement("tr");

        linha.innerHTML = `
            <td>${veiculo.nome}</td>
            <td>
                <input
                    type="number"
                    min="0"
                    data-id="${veiculo.id}"
                    value="${veiculo.quantidade}"
                    ${eAdministrador ? "" : "disabled"}
                >
            </td>
        `;

        corpoTabela.appendChild(linha);
    }
}

async function salvarEstoque() {
    const inputs = document.querySelectorAll("#corpoTabela input");
    const dados = [];

    for (const input of inputs) {
        dados.push({
            id: parseInt(input.dataset.id),
            quantidade: parseInt(input.value || "0")
        });
    }

    const resposta = await fetch("/api/veiculos?id_solicitante=" + idUsuario, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });
    const resultado = await resposta.json();

    document.getElementById("mensagem").textContent = resultado.mensagem;
    carregarEstoque();
}

// Sem permissão de administrador, nenhum botão aparece: apenas a mensagem.
if (!eAdministrador) {
    for (const botao of document.querySelectorAll("button")) {
        botao.style.display = "none";
    }
    document.getElementById("mensagem").textContent =
        "Apenas administradores podem alterar o estoque.";
}

carregarEstoque();