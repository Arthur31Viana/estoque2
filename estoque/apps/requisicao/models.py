from django.db import models
from django.urls import reverse_lazy
from estoque.apps.instituicao.models import Instituicao


class Requisicao(models.Model):
    requisicao = models.CharField('Nº Requisição', max_length=7)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT, null=True, blank=True)
    data = models.DateField('Data')
    documento = models.FileField('Requisição', upload_to='Requisições/%Y/%d-%m-%Y/')

    class Meta:
        verbose_name_plural = 'Requisições'
        verbose_name = 'Requisição'
        ordering = ['-data']

    def chage_view(self):
        return self.documento

    def __str__(self):
        return self.requisicao

    def get_absolute_url(self):
        return reverse_lazy('requisicao:requisicao_list')
