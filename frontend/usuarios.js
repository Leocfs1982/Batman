// A página é aberta pelo FastAPI, então usamos caminhos relativos.
const usuarioLogado = JSON.parse(localStorage.getItem("usuario_logado") || "null");
const eAdministrador = usuarioLogado && usuarioLogado.role === "admin";

async function carregarUsuarios() {
    const resposta = await fetch("/api/usuarios");
    const usuarios = await resposta.json();
    const corpoTabela = document.getElementById("corpoTabela");
    corpoTabela.innerHTML = "";

    for (const usuario of usuarios) {
        const linha = document.createElement("tr");
        const acoes = eAdministrador
            ? `<div class="acoes-linha">
                    <select data-id="${usuario.id}" onchange="alterarPermissao(this)">
                        <option value="usuario" ${usuario.role === "usuario" ? "selected" : ""}>Usuário</option>
                        <option value="admin" ${usuario.role === "admin" ? "selected" : ""}>Administrador</option>
                    </select>
                    <button onclick="excluirUsuario(${usuario.id})">Excluir</button>
                </div>`
            : `<span style="color:#999">Apenas administrador</span>`;

        linha.innerHTML = `
            <td>${usuario.id}</td>
            <td>${usuario.nome}</td>
            <td>${usuario.email}</td>
            <td>${usuario.senha}</td>
            <td>${usuario.role === "admin" ? "Administrador" : "Usuário"}</td>
            <td>${acoes}</td>
        `;
        corpoTabela.appendChild(linha);
    }
}

async function alterarPermissao(seletor) {
    const resposta = await fetch("/api/usuarios/role", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: parseInt(seletor.dataset.id),
            role: seletor.value,
            id_solicitante: usuarioLogado ? usuarioLogado.id : 0
        })
    });
    const resultado = await resposta.json();
    document.getElementById("mensagem").textContent = resultado.mensagem;
}

async function excluirUsuario(id) {
    if (!confirm("Deseja excluir este usuário?")) return;

    const resposta = await fetch("/api/usuarios/eliminar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: id,
            role: "",
            id_solicitante: usuarioLogado ? usuarioLogado.id : 0
        })
    });
    const resultado = await resposta.json();
    document.getElementById("mensagem").textContent = resultado.mensagem;
    carregarUsuarios();
}

carregarUsuarios();
