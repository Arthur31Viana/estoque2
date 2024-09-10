from ninja import ModelSchema

from .models import Produto


class ProdutoSchema(ModelSchema):

    class Meta:
        model = Produto
        fields = (
            'id',
            'produto',
            'estoque',
        )
