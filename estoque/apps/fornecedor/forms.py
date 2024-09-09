from django import forms
from .models import Fornecedor


class FornecedorFormAdmin(forms.ModelForm):

    class Meta:
        model = Fornecedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FornecedorFormAdmin, self).__init__(*args, **kwargs)
        self.fields['cnpj'].widget.attrs['class'] = 'mask-cnpj'
        self.fields['cep'].widget.attrs['class'] = 'mask-cep'
        self.fields['telefone'].widget.attrs['class'] = 'mask-telefone'
