from django import forms
from .models import Requisicao


class RequisicaoFormAdmin(forms.ModelForm):

    class Meta:
        model = Requisicao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequisicaoFormAdmin, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['class'] = 'mask-data'
        self.fields['requisicao'].widget.attrs['class'] = 'mask-requisicao'
