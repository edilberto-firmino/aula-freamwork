const formulario = document.getElementById("formCompra");

formulario.addEventListener("submit", function(event) {

    // Impede o formulário de recarregar a página
    event.preventDefault();

    // Pegando os valores dos campos
    const nome = document.getElementById("nome").value;
    const endereco = document.getElementById("endereco").value;
    const telefone = document.getElementById("telefone").value;
    const quantidade = document.getElementById("quantidade").value;
    const dataEntrega = document.getElementById("dataEntrega").value;
    const email = document.getElementById("email").value;
    const observacoes = document.getElementById("observacoes").value;

    // Formata a data
    const data = new Date(dataEntrega);

    const dataFormatada = data.toLocaleString("pt-BR");

    // Montando a mensagem
    const mensagem = `
🍔 NOVO PEDIDO

👤 Cliente: ${nome}

📍 Endereço:
${endereco}

📞 Telefone:
${telefone}

📦 Quantidade:
${quantidade}

📅 Data e hora da entrega:
${dataFormatada}

📧 E-mail:
${email}

📝 Observações:
${observacoes || "Nenhuma observação"}
`;

    // Remove tudo que não seja número
    let telefoneWhatsApp = telefone.replace(/\D/g, "");

    // Adiciona o código do Brasil
    if (!telefoneWhatsApp.startsWith("55")) {
        telefoneWhatsApp = "55" + telefoneWhatsApp;
    }

    // Codifica a mensagem para URL
    const mensagemCodificada = encodeURIComponent(mensagem);

    // Cria o link do WhatsApp
    const urlWhatsApp =
        `https://wa.me/${telefoneWhatsApp}?text=${mensagemCodificada}`;

    // Abre o WhatsApp
    window.open(urlWhatsApp, "_blank");

});