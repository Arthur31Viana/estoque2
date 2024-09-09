from django import forms
from .models import Estoque, EstoqueItens
from ..produto.models import Produto


class EstoqueFormAdmin(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = (
            'instituicao',
            'fornecedor',
            'nf',
            'modalidade',
            'requisicao',
            'data',
            'semana',
        )

    def __init__(self, *args, **kwargs):
        super(EstoqueFormAdmin, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['class'] = 'mask-data'
        self.fields['requisicao'].widget.attrs['class'] = 'mask-requisicao'


class EstoqueItensEntradaFormAdmin(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = (
            'estoque',
            'produto',
            'preco',
            'quantidade',
            'saldo',
        )

    def __init__(self, *args, **kwargs):
        super(EstoqueItensEntradaFormAdmin, self).__init__(*args, **kwargs)
        self.fields['preco'].widget.attrs['class'] = 'mask-preco'


class EstoqueItensSaidaFormAdmin(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = (
            'estoque',
            'produto',
            'quantidade_req',
            'quantidade',
            'saldo',
        )

    def __init__(self, *args, **kwargs):
        super(EstoqueItensSaidaFormAdmin, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior que zero
        self.fields['produto'].queryset = Produto.objects.filter(estoque__gt=0)
