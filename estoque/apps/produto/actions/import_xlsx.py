import xlrd
from estoque.apps.produto.models import Produto, Categoria


def import_xlsx(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    fields = ('produto', 'estoque', 'estoque_minimo', 'un_medida')

    categorias = []
    for row in range(1, sheet.nrows):
        categoria = sheet.row(row)[4].value
        categorias.append(categoria)

    categorias_unicas = [Categoria(categoria=categoria) for categoria in set(categorias) if categoria]

    Categoria.objects.bulk_create(categorias_unicas)

    aux = []
    for row in range(1, sheet.nrows):
        produto = sheet.row(row)[0].value
        estoque = sheet.row(row)[1].value
        estoque_minimo = sheet.row(row)[2].value
        un_medida = sheet.row(row)[3].value
        categoria = sheet.row(row)[4].value

        categoria = Categoria.objects.filter(categoria=categoria).first()

        produto = dict(
            produto=produto,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
            un_medida=un_medida,
        )

        if categoria:
            obj = Produto(categoria=categoria, **produto)
        else:
            obj = Produto(**produto)

        aux.append(obj)

    Produto.objects.bulk_create(aux)
