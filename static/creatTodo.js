function tratar_recv(data) {
    if (data["taskCreat"] == true) {
      $("#iconOK").addClass("fa-solid fa-circle-check");
      $("#msgOK").text("Tarefa Criada com sucesso!");
    } 
  }
  
  function createTodo_form() {
    val_todo = $('input[name="todo"]').val();
    val_descrition = $('input[name="todoDescription"]').val();
    val_start = $('input[name="startAt"]').val();
    val_end = $('input[name="endAt"]').val();
    json_send = { todo: val_todo, todoDescription: val_descrition, startAt : val_start, endAt : val_end };
    $.post($SCRIPT_ROOT + "/todo", json_send, tratar_recv, "json");
  }
  
  $(function () {
    $("#submit").click(createTodo_form);
  });