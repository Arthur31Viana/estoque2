import xlrd
from estoque.apps.instituicao.models import Instituicao


def import_xlsx(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    fields = (
        'instituicao',
        'denominacao',
        'inep',
        'diretora',
        'telefone',
        'email'
    )

    aux = []
    for row in range(1, sheet.nrows):
        instituicao = sheet.row(row)[0].value
        denominacao = sheet.row(row)[1].value
        inep = sheet.row(row)[2].value
        diretora = sheet.row(row)[3].value
        telefone = sheet.row(row)[4].value
        email = sheet.row(row)[5].value

        instituicao = dict(
            instituicao=instituicao,
            denominacao=denominacao,
            inep=inep,
            diretora=diretora,
            telefone=telefone,
            email=email,
        )

        obj = Instituicao(**instituicao)

        aux.append(obj)

    Instituicao.objects.bulk_create(aux)
