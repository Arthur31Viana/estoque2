//Mask
var SPMaskBehavior = function (val) {
  return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};

$(function(){
    //Adicionando Mask no html do django
    $('.mask-telefone').mask(SPMaskBehavior, spOptions);
    $('.mask-cnpj').mask('00.000.000/0000-00', {reverse: true});
    $('.mask-cep').mask('00000-000');
    $('.mask-data').mask('00/00/0000');
    $('.mask-requisicao').mask('24/0000');
});
