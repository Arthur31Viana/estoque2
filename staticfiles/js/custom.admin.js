//Mask
var SPMaskBehavior = function (val) {
  return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};

django.jQuery(function(){
    //Adicionando Mask no adimn do django
    django.jQuery('.mask-telefone').mask(SPMaskBehavior, spOptions);
    django.jQuery('.mask-cnpj').mask('00.000.000/0000-00', {reverse: true});
    django.jQuery('.mask-cep').mask('00000-000');
    django.jQuery('.mask-data').mask('00/00/0000');
});
