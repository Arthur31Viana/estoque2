from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.apps.fornecedor import views as v

app_name = 'fornecedor'

urlpatterns = [
    path('', login_required(v.FornecedorList.as_view()), name='fornecedor_list'),
    path('<int:pk>/', v.fornecedor_detail, name='fornecedor_detail'),
    path('nova-instituicao/', login_required(v.FornecedorCreate.as_view()), name='fornecedor_add'),
    path('<int:pk>/editar/', login_required(v.FornecedorUpdate.as_view()), name='fornecedor_edit'),
    path('<int:pk>/deletar/', login_required(v.FornecedorDelete.as_view()), name='fornecedor_delete'),
    path('import/xlsx/', v.import_xlsx, name='import_xlsx'),
    path('export/xlsx/', v.exportar_fornecedores_xlsx, name='export_xlsx'),
    path('<int:pk>/pdf/', v.ViewPDFDetail, name='fornecedor_pdf'),
]
