from ninja import ModelSchema

from .models import EstoqueItens


class EstoqueItemSchema(ModelSchema):

    class Meta:
        model = EstoqueItens
        fields = (
            'id',
            'produto',
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
