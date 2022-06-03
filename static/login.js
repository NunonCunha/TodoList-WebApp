/*
*Cria função que o receber o json do servidor verifica se na data vem true
*Caso a condição confirme executa o corpo da função
*Limpa apresenta icon e mensagens no html
*Caso a condição não redireciona a pagina
*/ 
function tratar_recv(data) {
  if (data["error"] == true) {
    $("#icon").addClass("fa-solid fa-circle-exclamation");
    $("#msgErro").text("Nome do utilizador ou palavra-passe inválido!");
  } else {
    $(location).prop("href", data["redirect"]);
  }
}

/*
*Cria função que recebe dados do formulario do htmll
*Cria um json e envia para o servidor
*/ 
function submeter_form() {
  valor_usr = $('input[name="email"]').val();
  valor_pwd = $('input[name="password"]').val();
  json_send = { email: valor_usr, password: valor_pwd };
  $.post($SCRIPT_ROOT + "/login", json_send, tratar_recv, "json");
}

/*
*Função associado ao botão do html 
*/
$(function () {
  $("#submit").click(submeter_form);
});
