// A página é aberta diretamente pelo FastAPI (http://localhost:8000/missoes),
// então usamos caminhos relativos (o frontend e o backend estão juntos).

// Dados do usuário logado salvos na tela de entrada (mesmo padrão da página de usuários).
const usuarioLogado = JSON.parse(localStorage.getItem("usuario_logado") || "null");
const idUsuario = usuarioLogado ? usuarioLogado.id : 0;
const eAdministrador = usuarioLogado && usuarioLogado.role === "admin";

async function carregarMissoes() {
    const resposta = await fetch("/api/missoes");
    const missoes = await resposta.json();

    const corpoTabela = document.getElementById("corpoTabela");
    corpoTabela.innerHTML = "";

    for (const missao of missoes) {
        const linha = document.createElement("tr");
        if (missao.concluida) {
            linha.classList.add("concluida");
        }
        linha.id = "linha-" + missao.id;

        linha.innerHTML = `
            <td class="check">
                <input
                    type="checkbox"
                    data-id="${missao.id}"
                    ${missao.concluida ? "checked" : ""}
                    ${eAdministrador ? "" : "disabled"}
                >
            </td>
            <td>${missao.nome}</td>
        `;

        corpoTabela.appendChild(linha);
    }
}

// Atualiza a linha visualmente quando o checkbox muda
async function salvarMissoes() {
    const checkboxes = document.querySelectorAll("#corpoTabela input[type=checkbox]");
    const dados = [];

    for (const cb of checkboxes) {
        dados.push({
            id: parseInt(cb.dataset.id),
            concluida: cb.checked
        });
    }

    const resposta = await fetch("/api/missoes?id_solicitante=" + idUsuario, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });
    const resultado = await resposta.json();

    document.getElementById("mensagem").textContent = resultado.mensagem;

    // Atualiza a marcação visual (risca a missão concluída)
    for (const cb of checkboxes) {
        document.getElementById("linha-" + cb.dataset.id).classList.toggle(
            "concluida",
            cb.checked
        );
    }
}

// Sem permissão de administrador, nenhum botão aparece: apenas a mensagem.
if (!eAdministrador) {
    for (const botao of document.querySelectorAll("button")) {
        botao.style.display = "none";
    }
    document.getElementById("mensagem").textContent =
        "Apenas administradores podem marcar missões como concluídas.";
}

carregarMissoes();