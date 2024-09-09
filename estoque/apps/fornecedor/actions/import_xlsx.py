import xlrd
from estoque.apps.fornecedor.models import Fornecedor


def import_xlsx(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    fields = (
        'Razao_Social',
        'Nome_Fantasia',
        'cnpj',
        'Inscricao_Municipal',
        'Inscricao_Estadual',
        'UF',
        'Cidade',
        'Bairro',
        'Logradouro',
        'Numero',
        'cep',
        'telefone',
        'email'
    )

    aux = []
    for row in range(1, sheet.nrows):
        Razao_Social = sheet.row(row)[0].value
        Nome_Fantasia = sheet.row(row)[1].value
        cnpj = sheet.row(row)[2].value
        Inscricao_Municipal = sheet.row(row)[3].value
        Inscricao_Estadual = sheet.row(row)[4].value
        UF = sheet.row(row)[5].value
        Cidade = sheet.row(row)[6].value
        Bairro = sheet.row(row)[7].value
        Logradouro = sheet.row(row)[8].value
        Numero = sheet.row(row)[9].value
        cep = sheet.row(row)[10].value
        telefone = sheet.row(row)[11].value
        email = sheet.row(row)[12].value

        fornecedor = dict(
            Razao_Social=Razao_Social,
            Nome_Fantasia=Nome_Fantasia,
            cnpj=cnpj,
            Inscricao_Municipal=Inscricao_Municipal,
            Inscricao_Estadual=Inscricao_Estadual,
            UF=UF,
            Cidade=Cidade,
            Bairro=Bairro,
            Logradouro=Logradouro,
            Numero=Numero,
            cep=cep,
            telefone=telefone,
            email=email,
        )

        obj = Fornecedor(**fornecedor)

        aux.append(obj)

    Fornecedor.objects.bulk_create(aux)
