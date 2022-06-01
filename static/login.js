function tratar_recv(data){
    if (data['error'] == true){
        $("#icon").addClass("fa-solid fa-circle-exclamation");
        $("#msgErro").text("Nome do utilizador ou palavra-passe inválido!");
    }
}

function submeter_form(){
    valor_usr = $('input[name="email"]').val();
    valor_pwd = $('input[name="password"]').val();
    json_send = {email: valor_usr, password: valor_pwd};
    $.post($SCRIPT_ROOT + '/login', json_send, tratar_recv, 'json');
}

$(function() {
    $('#submit').click(submeter_form);
});