import xlrd
from estoque.apps.estoques.models import Estoque
from estoque.apps.estoques.models import EstoqueItens


def import_xlsx(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    fields = ('produto', 'quantidade', 'saldo')

    estoques = []
    for row in range(1, sheet.nrows):
        estoque = sheet.row(row)[0].value
        estoques.append(estoque)

    estoques_unicos = [Estoque(estoque=estoque) for estoque in set(estoques) if estoque]

    Estoque.objects.bulk_create(estoques_unicos)

    aux = []
    for row in range(1, sheet.nrows):
        estoque.funcionario.first_name = sheet.row(row)[0].value
        estoque.funcionario.last_name = sheet.row(row)[1].value
        estoque.instituicao.instituicao = sheet.row(row)[2].value
        estoque.fornecedor.Razao_Social = sheet.row(row)[3].value
        estoque.nf = sheet.row(row)[4].value
        estoque.modalidade = sheet.row(row)[5].value
        estoque.requisicao = sheet.row(row)[6].value
        estoque.movimento = sheet.row(row)[7].value
        produto = sheet.row(row)[8].value
        quantidade = sheet.row(row)[9].value
        saldo = sheet.row(row)[10].value

        estoque = EstoqueItens.objects.filter(estoque=estoque).first()

        estoque = dict(
            estoque=estoque,
            produto=produto,
            quantidade=quantidade,
            saldo=saldo,
        )

        if estoque:
            obj = EstoqueItens(estoque=estoque, **estoque)
        else:
            obj = EstoqueItens(**estoque)

        aux.append(obj)

    EstoqueItens.objects.bulk_create(aux)
