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
  
  function createTodo_form() {
    val_todo = $('input[name="todo"]').val();
    val_descrition = $('input[name="todoDescription"]').val();
    val_start = $('input[name="startAt"]').val();
    val_end = $('input[name="endAt"]').val();
    if ((val_todo != "") || (val_descrition != "") || (val_start != "") || (val_end != "") ) {
        json_send = { todo: val_todo, todoDescription: val_descrition, startAt : val_start, endAt : val_end };
        $.post($SCRIPT_ROOT + "/todo", json_send, tratar_recv, "json");}
    else {
        $("#icon").addClass("fa-solid fa-circle-exclamation");
        $("#msgErro").text("Todos os campos são obrigatórios!");
    }
  }
  
  $(function () {
    $("#submit").click(createTodo_form);
  });