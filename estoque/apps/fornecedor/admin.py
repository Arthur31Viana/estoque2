from django.contrib import admin
from .forms import FornecedorFormAdmin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    form = FornecedorFormAdmin

    class Media:
        js = (
            'js/jquery/jquery.mask.min.js',
            'js/custom.admin.js',
        )
