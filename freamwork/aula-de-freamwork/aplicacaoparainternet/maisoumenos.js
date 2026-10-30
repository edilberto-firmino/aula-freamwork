const formulario = document.getElementById("formCadastro");

formulario.addEventListener("submit", function(event) {

    // Impede a página de recarregar
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;

    const mensagem = document.getElementById("mensagem");


    // Verifica se algum campo está vazio
    if (
        nome === "" ||
        email === "" ||
        senha === "" ||
        confirmarSenha === ""
    ) {

        mensagem.innerText = "Preencha todos os campos.";
        mensagem.style.color = "red";

        return;
    }


    // Verifica tamanho da senha
    if (senha.length < 6) {

        mensagem.innerText = "A senha deve ter pelo menos 6 caracteres.";
        mensagem.style.color = "red";

        return;
    }


    // Verifica se as senhas são iguais
    if (senha !== confirmarSenha) {

        mensagem.innerText = "As senhas não são iguais.";
        mensagem.style.color = "red";

        return;
    }


    // Cadastro realizado
    mensagem.innerText = "Cadastro realizado com sucesso!";
    mensagem.style.color = "green";


    // Limpa o formulário
    formulario.reset();

});