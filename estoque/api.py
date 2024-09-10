from ninja import NinjaAPI

api = NinjaAPI()

api.add_router('', 'estoque.apps.estoques.api.router')
api.add_router('', 'estoque.apps.produto.api.router')
