from django.shortcuts import get_object_or_404

from ninja import Router

from .models import EstoqueSaida, EstoqueItens
from .schemas import EstoqueItemSchema, EstoqueItemUpdateSchema


router = Router(tags=['EstoqueSaida'])


@router.get('estoque-saida/{pk}', response=list[EstoqueItemSchema])
def estoque_saida(request, pk: int):
    estoque = get_object_or_404(EstoqueSaida, pk=pk)
    items = EstoqueItens.objects.filter(estoque=estoque)
    return items


@router.patch('estoque-saida-item/{pk}')
def estoque_saida_itens_update(request, pk: int, payload: EstoqueItemUpdateSchema):
    instance = get_object_or_404(EstoqueItens, pk=pk)
    data = payload.dict()

    for attr, value in data.items():
        setattr(instance, attr, value)

    instance.save()

    return {'status': 'ok'}
