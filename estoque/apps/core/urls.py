from django.urls import path
from estoque.apps.core import views as v

app_name = 'core'

urlpatterns = [
    path('', v.index, name='index'),
]
