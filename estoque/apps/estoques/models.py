from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models import F
from django.db import models
from estoque.apps.core.models import TimeStampedModel
from estoque.apps.produto.models import Produto
from estoque.apps.instituicao.models import Instituicao
from estoque.apps.fornecedor.models import Fornecedor
from .managers import EstoqueEntradaManager, EstoqueSaidaManager


MOVIMENTO = (
    ('e', 'Entrada'),
    ('s', 'Saída'),
)


class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True
    )
    instituicao = models.ForeignKey(
        Instituicao,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    nf = models.CharField(
        'Nota Fiscal',
        max_length=20,
        null=True,
        blank=True
    )
    modalidade = models.CharField(
        'Modalidade',
        max_length=100,
        null=True,
        blank=True
    )
    requisicao = models.CharField(
        'Nº Requisição',
        max_length=7,
        null=True,
        blank=True
    )
    movimento = models.CharField(
        'Movimento',
        max_length=1,
        choices=MOVIMENTO,
        blank=True
    )
    data = models.DateField('Data', null=True, blank=True)
    semana = models.CharField('Semana', max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = 'Estoque'
        ordering = ('-data',)

    def __str__(self):
        if self.nf:
            return '{} - {} - {}'.format(self.pk, self.nf, self.data)
        return '{} --- {}'.format(self.pk, self.data)

    def nf_formated(self):
        if self.nf:
            return str(self.nf).zfill(3)
        return '---'


class EstoqueEntrada(Estoque):
    objects = EstoqueEntradaManager()

    class Meta:
        proxy = True
        verbose_name = 'Estoque de Entrada'
        verbose_name_plural = 'Estoque de Entradas'


class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManager()

    class Meta:
        proxy = True
        verbose_name = 'Estoque de Saída'
        verbose_name_plural = 'Estoque de Saídas'


class EstoqueItens(models.Model):
    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.CASCADE,
        related_name='estoques'
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(
        'Preço Unitário',
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    total = models.DecimalField(
        'Preço Total',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False
    )
    quantidade_req = models.PositiveIntegerField('Quantidade Requerida', null=True, blank=True)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField('Saldo em Estoque', blank=True)

    class Meta:
        verbose_name = 'Estoque Itens'
        ordering = ('pk',)

    def save(self, *args, **kwargs):
        if self.estoque.movimento == 'e':
            self.total = self.quantidade * self.preco
        super(EstoqueItens, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.produto)
