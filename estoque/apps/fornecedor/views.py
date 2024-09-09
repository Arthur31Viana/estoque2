from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from xhtml2pdf import pisa
from estoque.apps.fornecedor.actions.export_xlsx import export_xlsx
from estoque.apps.fornecedor.actions.import_xlsx import (
    import_xlsx as action_import_xlsx
)
from .models import Fornecedor
from .forms import FornecedorFormAdmin


class FornecedorList(ListView):
    model = Fornecedor
    template_name = 'fornecedor_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(Razao_Social__icontains=search)
                |Q(cnpj__icontains=search)
            )
        return qs


@login_required
def fornecedor_detail(request, pk):
    template_name = 'fornecedor_detail.html'
    obj = Fornecedor.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


class FornecedorCreate(CreateView):
    form_class = FornecedorFormAdmin
    template_name = 'fornecedor_form.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            "Fornecedor Adicionado com Sucesso!"
        )
        return super(FornecedorCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro! Verifique se todos os campos estão preenchidos!"
        )
        return super(FornecedorCreate, self).form_invalid(form)


class FornecedorUpdate(UpdateView):
    model = Fornecedor
    fields = ('__all__')
    template_name = 'fornecedor_form.html'


class FornecedorDelete(DeleteView):
    model = Fornecedor
    template_name = 'fornecedor_confirm_delete.html'
    success_url = reverse_lazy('fornecedor:fornecedor_list')


@login_required
def import_xlsx(request):
    filename = 'fix/fornecedores.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Fornecedores Importados com Sucesso!')
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(reverse('fornecedor:fornecedor_list'))


@login_required
def exportar_fornecedores_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Fornecedor'
    filename = 'fornecedores_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Fornecedor.objects.all().values_list(
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
        'email',
    )
    columns = ('Razão Social', 'Nome Fantasia', 'CNPJ', 'Insc. Municipal',
               'Insc. Estadual', 'UF', 'Cidade', 'Bairro', 'Logradouro',
               'Número', 'CEP', 'Telefone', 'E-mail')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response


def ViewPDFDetail(request, *args, **kwargs):
    pk = kwargs.get('pk')
    fornecedor = get_object_or_404(Fornecedor, pk=pk)

    template_path = 'fornecedor_pdf.html'
    context = {
        'object': fornecedor
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="fornecedor_pdf.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros <pre>' + html + '</pre>')
    return response
