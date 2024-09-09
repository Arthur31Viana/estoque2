from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.apps.instituicao import views as v

app_name = 'instituicao'

urlpatterns = [
    path('', login_required(v.InstituicaoList.as_view()), name='instituicao_list'),
    path('<int:pk>/', v.instituicao_detail, name='instituicao_detail'),
    path('nova-instituicao/', login_required(v.InstituicaoCreate.as_view()), name='instituicao_add'),
    path('<int:pk>/editar/', login_required(v.InstituicaoUpdate.as_view()), name='instituicao_edit'),
    path('<int:pk>/deletar/', login_required(v.InstituicaoDelete.as_view()), name='instituicao_delete'),
    path('import/xlsx/', v.import_xlsx, name='import_xlsx'),
    path('export/xlsx/', v.exportar_instituicoes_xlsx, name='export_xlsx'),
    path('<int:pk>/pdf/', v.ViewPDFDetail, name='instituicao_pdf'),
]
