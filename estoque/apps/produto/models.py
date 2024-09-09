from django.db import models
from django.urls import reverse_lazy


class Produto(models.Model):
    Quilograma = 'kg'
    Hectograma = 'hg'
    Decagrama = 'dag'
    Grama = 'g'
    Decigrama = 'dg'
    Centigrama = 'cg'
    Miligrama = 'mg'
    Quilolitro = 'kl'
    Hectolitro = 'hl'
    Decalitro = 'dal'
    Litro = 'l'
    Decilitro = 'dl'
    Centilitro = 'cl'
    Mililitro = 'ml'
    Milheiro = 'mil'
    Caixa = 'cx'
    Duzia = 'dz'
    Fardo = 'fd'
    Saco = 'sc'
    Unidade = 'und.'
    un_medida_choices = [
        (Quilograma, 'kg'),
        (Hectograma, 'hg'),
        (Decagrama, 'dag'),
        (Grama, 'g'),
        (Decigrama, 'dg'),
        (Centigrama, 'cg'),
        (Miligrama, 'mg'),
        (Quilolitro, 'kl'),
        (Hectolitro, 'hl'),
        (Decalitro, 'dal'),
        (Litro, 'l'),
        (Decilitro, 'dl'),
        (Centilitro, 'cl'),
        (Mililitro, 'ml'),
        (Milheiro, 'mil'),
        (Caixa, 'cx'),
        (Duzia, 'dz'),
        (Fardo, 'fd'),
        (Saco, 'sc'),
        (Unidade, 'und.'),
    ]
    produto = models.CharField(
        'Produto',
        max_length=100,
        unique=True
    )
    estoque = models.FloatField('Estoque Atual')
    estoque_minimo = models.PositiveIntegerField('Estoque Mínimo', default=0)
    un_medida = models.CharField(
        'Unidade de Medida',
        max_length=4,
        choices=un_medida_choices,
        default=Quilograma
    )
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Produtos'
        verbose_name = 'Produto'
        ordering = ['produto']

    def __str__(self):
        return self.produto

    def get_absolute_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.pk})

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
        }


class Categoria(models.Model):
    categoria = models.CharField('Categoria', max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categorias'
        verbose_name = 'Categoria'
        ordering = ['categoria']

    def __str__(self):
        return self.categoria
