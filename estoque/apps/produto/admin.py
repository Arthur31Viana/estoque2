from django.contrib import admin
from .models import Produto, Categoria


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'categoria',
        'estoque',
        'estoque_minimo',
        'un_medida',
    )
    search_fields = ('produto',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        'categoria',
    )
    search_fields = ('categoria',)
