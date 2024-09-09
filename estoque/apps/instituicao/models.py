from django.db import models
from django.urls import reverse_lazy


class Instituicao(models.Model):
    instituicao = models.CharField('Instituição', max_length=100)
    denominacao = models.CharField('Denominação', max_length=100, null=True, blank=True)
    inep = models.IntegerField('INEP', unique=True)
    diretora = models.CharField('Diretor(a)', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.EmailField('E-mail')

    class Meta:
        verbose_name_plural = 'Instituições'
        verbose_name = 'Instituição'
        ordering = ['instituicao']

    def __str__(self):
        return self.instituicao + ' - ' + str(self.denominacao)

    def get_absolute_url(self):
        return reverse_lazy('instituicao:instituicao_detail', kwargs={'pk': self.pk})
