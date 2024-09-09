from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.apps.produto import views as v

app_name = 'produto'

urlpatterns = [
    path('', login_required(v.ProdutoList.as_view()), name='produto_list'),
    path('<int:pk>/', v.produto_detail, name='produto_detail'),
    path('novo-produto/', login_required(v.ProdutoCreate.as_view()), name='produto_add'),
    path('<int:pk>/editar/', login_required(v.ProdutoUpdate.as_view()), name='produto_edit'),
    path('<int:pk>/deletar/', login_required(v.ProdutoDelete.as_view()), name='produto_delete'),
    path('<int:pk>/json/', v.produto_json, name='produto_json'),
    path('import/xlsx/', v.import_xlsx, name='import_xlsx'),
    path('export/xlsx/', v.exportar_produtos_xlsx, name='export_xlsx'),
    path('<int:pk>/pdf/', v.ViewPDFDetail, name='produto_pdf'),
]
