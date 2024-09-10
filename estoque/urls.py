from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path


from .api import api


urlpatterns = [
    path('', include('estoque.apps.core.urls')),
    path('instituicao/', include('estoque.apps.instituicao.urls')),
    path('fornecedor/', include('estoque.apps.fornecedor.urls')),
    path('produto/', include('estoque.apps.produto.urls')),
    path('estoque/', include('estoque.apps.estoques.urls')),
    path('requisicao/', include('estoque.apps.requisicao.urls')),
    path('api/v1/', api.urls),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
