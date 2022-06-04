/*
 *Cria função que o receber o json do servidor verifica se na data vem true
 *Caso a condição confirme executa o corpo da função
 *Limpa valores do formuario e apresenta icons e mensagens no html
 */
function tratar_recv(data) {
  if (data["taskCreat"] == true) {
    $("#iconOK").addClass("fa-solid fa-circle-check");
    $("#msgOK").text("Tarefa Criada com sucesso!");
    $('input[name="todo"]').val(null);
    $('input[name="todoDescription"]').val(null);
    $('input[name="startAt"]').val(null);
    $('input[name="endAt"]').val(null);
    $(".ok").append("<p></p>");
  }
}

/*
 *Cria função recebe dados do formulario do html
 *Feito condição para validar se existe informação em todos os campos do formulario
 *Se a condição não for cumprida apresenta uma mensagem no html
 *Se a confição for cumprida cria um json e envia para o servidor
 */

function createTodo_form() {
  val_todo = $('input[name="todo"]').val();
  val_descrition = $('input[name="todoDescription"]').val();
  val_start = $('input[name="startAt"]').val();
  val_end = $('input[name="endAt"]').val();
  if (
    val_todo != "" &&
    val_descrition != "" &&
    val_start != "" &&
    val_end != ""
  ) {
    json_send = {
      todo: val_todo,
      todoDescription: val_descrition,
      startAt: val_start,
      endAt: val_end,
    };
    $.post($SCRIPT_ROOT + "/todo", json_send, tratar_recv, "json");
  } else {
    $("#icon").addClass("fa-solid fa-circle-exclamation");
    $("#msgErro").text("Todos os campos são obrigatórios!");
  }
}

/*
 *Função associado ao botão do html
 */

$(function () {
  $("#submit").click(createTodo_form);
});
