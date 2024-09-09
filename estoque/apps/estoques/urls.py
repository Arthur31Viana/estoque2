from django.urls import include, path
from django.contrib.auth.decorators import login_required
from estoque.apps.estoques import views as v

app_name = 'estoque'

entrada_patterns = [
    path('', login_required(v.EstoqueEntradaList.as_view()), name='estoque_entrada_list'),
    path('nova-entrada/', v.estoque_entrada_add, name='estoque_entrada_add'),
    path('<int:pk>/pdf/', v.ViewPDFDetail, name='entrada_pdf'),
]

saida_patterns = [
    path('', login_required(v.EstoqueSaidaList.as_view()), name='estoque_saida_list'),
    path('nova-saida/', v.estoque_saida_add, name='estoque_saida_add'),
    path('requisicao/<int:pk>/', v.ViewPDFRequisicao, name='requisicao_pdf'),
]

urlpatterns = [
    path('<int:pk>/', login_required(v.EstoqueDetail.as_view()), name='estoque_detail'),
    path('<int:pk>/deletar/', login_required(v.EstoqueDelete.as_view()), name='estoque_delete'),
    path('entrada/', include(entrada_patterns)),
    path('saida/', include(saida_patterns)),
    path('import/xlsx/', v.import_xlsx, name='import_xlsx'),
    path('export/xlsx/', v.exportar_xlsx, name='export_xlsx'),
]
