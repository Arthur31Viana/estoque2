from django import forms
from .models import Instituicao


class InstituicaoFormAdmin(forms.ModelForm):

    class Meta:
        model = Instituicao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InstituicaoFormAdmin, self).__init__(*args, **kwargs)
        self.fields['telefone'].widget.attrs['class'] = 'mask-telefone'
