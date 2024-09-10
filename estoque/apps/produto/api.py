from ninja import Router

from .models import Produto
from .schemas import ProdutoSchema


router = Router(tags=['Produto'])


@router.get('produtos', response=list[ProdutoSchema])
def list_produto(request):
    return Produto.objects.all()


@router.get('produtos/{pk}', response=ProdutoSchema)
def get_produto(request, pk: int):
    return Produto.objects.get(pk=pk)
