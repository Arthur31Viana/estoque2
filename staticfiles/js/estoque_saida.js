$(document).ready(function() {
    // Insere classe no primeiro item de produto
    $('#id_estoque-0-produto').addClass('clProduto');
    $('#id_estoque-0-quantidade').addClass('clQuantidade');
    $('#id_estoque-0-quantidade_req').addClass('clQuantidadeReq');
    // Desabilita o primeiro campo 'saldo'
    $('#id_estoque-0-saldo').prop('type', 'hidden')
    //Cria um span para mostrar o saldo na tela
    $('label[for="id_estoque-0-saldo"]').append('<span id="id_estoque-0-saldo-span" class="lead"></span>')
    //Cria um campo com estoque inicial
    $('label[for="id_estoque-0-saldo"]').append('<input type="hidden" id="id_estoque-0-inicial"></span>')

    $('#add-item').click(function(ev) {
        ev.preventDefault();
        var count = $('#estoque').children().length;
        var tmplMarkup = $('#item-estoque').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#estoque').append(compiledTmpl);

        // update form count
        $('#id_estoque-TOTAL_FORMS').attr('value', count + 1);

        // Desabilitar o campo 'saldo'
        $('#id_estoque-' + (count) + '-saldo').prop('type', 'hidden')

        // some animate to scroll to view our new form
        $('html, body').animate({
            scrollTop: $("#add-item").position().top - 200
        }, 800);

        $('#id_estoque-' + (count) + '-produto').addClass('clProduto');
        $('#id_estoque-' + (count) + '-quantidade').addClass('clQuantidade');
        $('#id_estoque-' + (count) + '-quantidade_req').addClass('clQuantidadeReq');

        //Cria uma classe para label de produto
        $('label[for="id_estoque-' + (count) + '-produto"]').addClass('lbProduto')
        //Cria uma classe para label de quantidade
        $('label[for="id_estoque-' + (count) + '-quantidade"]').addClass('lbQuantidade')
        //Cria uma classe para label de quantidade
        $('label[for="id_estoque-' + (count) + '-quantidade_req"]').addClass('lbQuantidadeReq')

        //Cria um span para mostrar o saldo na tela
        $('label[for="id_estoque-' + (count) + '-saldo"]').append('<span id="id_estoque-' + (count) + '-saldo-span" class="lead"></span>')
        //Cria um campo com estoque inicial
        $('label[for="id_estoque-' + (count) + '-saldo"]').append('<input type="hidden" id="id_estoque-' + (count) + '-inicial"></span>')
    });
});

let estoque
let saldo
let campo
let campo2
let quantidade

$(document).on('change', '.clProduto', function() {
    let self = $(this)
    let pk = $(this).val()
    let url = '/produto/' + pk + '/json/'

    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            estoque = response.data[0].estoque
            campo = self.attr('id').replace('produto', 'quantidade')
            estoque_inicial = self.attr('id').replace('produto', 'inicial')
            // Estoque Inicial
            $('#'+estoque_inicial).val(estoque)
            // Remove o valor do campo quantidade
            $('#'+campo).val('')
        },
        error: function(xhr) {

        }
    })
});

$(document).on('change', '.clQuantidade', function() {
    quantidade = $(this).val();
    // Cálculo de soma do estoque
    campo = $(this).attr('id').replace('quantidade', 'saldo')
    campo_estoque_inicial = $(this).attr('id').replace('quantidade', 'inicial')
    estoque_inicial = $('#'+campo_estoque_inicial).val()
    saldo = Number(estoque_inicial) - Number(quantidade);
    if (saldo < 0) {
        alert('O Saldo não pode ser negativo.')
        // Atribui o saldo ao campo 'saldo'
        $('#'+campo).val('')
        return
    }
    // Atribue saldo ao campo saldo
    $('#'+campo).val(saldo)
    campo2 = $(this).attr('id').replace('quantidade', 'saldo-span')
    // Atribue o saldo ao campo 'id_estoque-x-saldo-span'
    $('#'+campo2).text(saldo)
});
