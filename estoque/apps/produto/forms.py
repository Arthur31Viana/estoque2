from django import forms
from .models import Produto


class ProdutoFormAdmin(forms.ModelForm):

    class Meta:
        model = Produto
        fields = [
            'produto',
            'categoria',
            'estoque',
            'un_medida',
        ]
