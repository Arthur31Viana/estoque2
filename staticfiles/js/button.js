// Botão de fechar alerta
$('.close-btn').click(function(){
    $('.alert').addClass("hide");
    $('.alert').removeClass("show");
});

// Esconde Botão automatico em 5 Segundos
setTimeout(function(){
    $('.alert').addClass("hide");
    $('.alert').removeClass("show");
},5000);
