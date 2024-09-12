from ninja import ModelSchema

from .models import EstoqueItens
from estoque.apps.produto.schemas import ProdutoSchema


class EstoqueItemSchema(ModelSchema):
    produto: ProdutoSchema

    class Meta:
        model = EstoqueItens
        fields = (
            'id',
            'quantidade_req',
            'quantidade',
            'saldo',
        )


class EstoqueItemUpdateSchema(ModelSchema):
    produto_id: int

    class Meta:
        model = EstoqueItens
        fields = (
            'quantidade_req',
            'quantidade',
            'saldo',
        )
