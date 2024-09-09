from django.db import models
from django.urls import reverse_lazy


class Fornecedor(models.Model):
    razao_soc = models.CharField('Razão Social', max_length=100, name='Razao_Social')
    nome_fant = models.CharField('Nome Fantasia', max_length=100, name='Nome_Fantasia')
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    insc_munic = models.CharField('Inscrição Municipal', max_length=100, name='Inscricao_Municipal')
    insc_estad = models.CharField('Inscrição Estadual', max_length=100, name='Inscricao_Estadual')
    uf = models.CharField('UF', max_length=2, name='UF')
    cidade = models.CharField('Cidade', max_length=100, name='Cidade')
    bairro = models.CharField('Bairro', max_length=100, name='Bairro')
    logradouro = models.CharField('Logradouro', max_length=100, name='Logradouro')
    numero = models.IntegerField('Número', name='Numero')
    cep = models.CharField('CEP', max_length=9)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.EmailField('E-mail')

    class Meta:
        verbose_name_plural = 'Fornecedores'
        verbose_name = 'Fornecedor'
        ordering = ['Razao_Social']

    def __str__(self):
        return self.Razao_Social

    def get_absolute_url(self):
        return reverse_lazy('fornecedor:fornecedor_detail', kwargs={'pk': self.pk})
