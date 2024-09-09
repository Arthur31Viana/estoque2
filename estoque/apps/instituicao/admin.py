from django.contrib import admin
from .forms import InstituicaoFormAdmin
from .models import Instituicao


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    form = InstituicaoFormAdmin

    class Media:
        js = (
            'js/jquery/jquery.mask.min.js',
            'js/custom.admin.js',
        )
