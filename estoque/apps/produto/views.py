from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from xhtml2pdf import pisa

from estoque.apps.produto.actions.export_xlsx import export_xlsx
from estoque.apps.produto.actions.import_xlsx import (
    import_xlsx as action_import_xlsx
)
from .models import Produto
from .forms import ProdutoFormAdmin


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(produto__icontains=search)
                |Q(categoria__categoria__icontains=search)
            )
        return qs


@login_required
def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


@login_required
def produto_add(request):
    template_name = 'produto_form.html'
    return render(request, template_name)


class ProdutoCreate(CreateView):
    form_class = ProdutoFormAdmin
    template_name = 'produto_form.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            "Produto Adicionado com Sucesso!"
        )
        return super(ProdutoCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro! Verifique se todos os campos estão preenchidos!"
        )
        return super(ProdutoCreate, self).form_invalid(form)


class ProdutoUpdate(UpdateView):
    model = Produto
    fields = ('__all__')
    template_name = 'produto_form.html'


class ProdutoDelete(DeleteView):
    model = Produto
    template_name = 'produto_confirm_delete.html'
    success_url = reverse_lazy('produto:produto_list')


def produto_json(request, pk):
    ''' Retorna o produto, id e estoque '''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})


@login_required
def import_xlsx(request):
    filename = 'fix/produtos.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Produtos Importados com Sucesso!')
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(reverse('produto:produto_list'))


@login_required
def exportar_produtos_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Produto'
    filename = 'produtos_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Produto.objects.all().values_list(
        'produto',
        'estoque',
        'estoque_minimo',
        'un_medida',
        'categoria__categoria',
    )
    columns = ('Produto', 'Estoque', 'Estoque Mínimo',
               'Uni. de Medida', 'Categoria')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response


def ViewPDFDetail(request, *args, **kwargs):
    pk = kwargs.get('pk')
    produto = get_object_or_404(Produto, pk=pk)

    template_path = 'produto_pdf.html'
    context = {
        'object': produto
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="produto_pdf.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros <pre>' + html + '</pre>')
    return response
