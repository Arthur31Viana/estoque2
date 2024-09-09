from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.apps.requisicao import views as v

app_name = 'requisicao'

urlpatterns = [
    path('', login_required(v.RequisicaoList.as_view()), name='requisicao_list'),
    path('nova-requisicao/', login_required(v.RequisicaoCreate.as_view()), name='requisicao_add'),
    path('<int:pk>/editar/', login_required(v.RequisicaoUpdate.as_view()), name='requisicao_edit'),
    path('<int:pk>/deletar/', login_required(v.RequisicaoDelete.as_view()), name='requisicao_delete'),
]
