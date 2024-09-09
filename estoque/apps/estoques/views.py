from datetime import datetime
from django.contrib import messages
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from xhtml2pdf import pisa

from estoque.apps.estoques.actions.export_xlsx import export_xlsx
from estoque.apps.estoques.actions.import_xlsx import (
    import_xlsx as action_import_xlsx
)
from estoque.apps.produto.models import Produto
from .models import Estoque, EstoqueEntrada, EstoqueSaida, EstoqueItens
from .forms import EstoqueFormAdmin, EstoqueItensEntradaFormAdmin, EstoqueItensSaidaFormAdmin


class EstoqueEntradaList(ListView):
    model = EstoqueEntrada
    template_name = 'estoque_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(funcionario__first_name__icontains=search)
                | Q(nf__icontains=search)
                | Q(created__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super(EstoqueEntradaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Entrada'
        context['url_add'] = 'estoque:estoque_entrada_add'
        context['url_requisicao'] = 'estoque:requisicao_entrada'
        return context


class EstoqueDetail(DetailView):
    model = Estoque
    template_name = 'estoque_detail.html'


class EstoqueDelete(DeleteView):
    model = Estoque
    template_name = 'estoque_confirm_delete.html'
    success_url = reverse_lazy('estoque:estoque_list')


def dar_baixa_estoque(form):
    # Pega os produtos a partir da instância do formulário estoque
    produtos = form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.estoque = item.saldo
        produto.save()
    print('Estoque Atualizado com Sucesso!')


def estoque_add(request, form_inline, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form=form_inline,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueFormAdmin(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            request.POST,
            instance=estoque_form,
            prefix='estoque'
        )
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=False)
            form.funcionario = request.user
            form.movimento = movimento
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            if movimento == 'e':
                messages.success(
                    request,
                    "Entrada de Produto Feita com Sucesso!"
                )
            else:
                messages.success(
                    request,
                    "Saída de Produto Feita  com Sucesso!"
                )
            return {'pk': form.pk}
        else:
            messages.error(
                request,
                "Erro! Verifique se todos os campos estão preenchidos!"
            )
    else:
        form = EstoqueFormAdmin(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')

    context = {'form': form, 'formset': formset}
    return context


def estoque_entrada_add(request):
    form_inline = EstoqueItensEntradaFormAdmin
    template_name = 'estoque_entrada_form.html'
    movimento = 'e'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, form_inline, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def ViewPDFDetail(request, *args, **kwargs):
    pk = kwargs.get('pk')
    object = get_object_or_404(EstoqueEntrada, pk=pk)

    template_path = 'entrada_pdf.html'
    context = {
        'object': object
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="entrada_pdf.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros <pre>' + html + '</pre>')
    return response


class EstoqueSaidaList(ListView):
    model = EstoqueSaida
    template_name = 'estoque_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(funcionario__first_name__icontains=search)
                | Q(funcionario__last_name__icontains=search)
                | Q(requisicao__icontains=search)
                | Q(created__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super(EstoqueSaidaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Saída'
        context['url_add'] = 'estoque:estoque_saida_add'
        return context


def estoque_saida_add(request):
    form_inline = EstoqueItensSaidaFormAdmin
    template_name = 'estoque_saida_form.html'
    movimento = 's'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, form_inline, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def estoque_saida_update(request, pk):
    template_name = 'estoque_saida_update_form.html'
    # movimento = 's'
    # url = 'estoque:estoque_detail'

    obj = get_object_or_404(Estoque, pk=pk)

    form = EstoqueFormAdmin(request.POST or None, instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('estoque:estoque_detail', pk=obj.pk)

    # context = estoque_add(request, template_name, movimento, url)
    context = {'object': obj, 'form': form}
    return render(request, template_name, context)


def ViewPDFRequisicao(request, *args, **kwargs):
    pk = kwargs.get('pk')
    object = get_object_or_404(Estoque, pk=pk)

    template_path = 'requisicao.html'
    context = {
        'object': object
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="requisicao.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros <pre>' + html + '</pre>')
    return response


@login_required
def import_xlsx(request):
    filename = 'fix/estoques.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Estoques Importados com Sucesso!')
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(reverse('estoque:estoque_entrada_list'))


@login_required
def exportar_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'EstoqueItens'
    filename = 'estoques_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = EstoqueItens.objects.all().values_list(
        'estoque__funcionario__first_name',
        'estoque__funcionario__last_name',
        'estoque__instituicao__instituicao',
        'estoque__fornecedor__Razao_Social',
        'estoque__nf',
        'estoque__modalidade',
        'estoque__requisicao',
        'estoque__movimento',
        'produto',
        'quantidade',
        'saldo',
    )
    columns = ('Funcionário(Primeiro Nome)', 'Funcionário(Último Nome)', 'Instituição', 'Fornecedor', 'Nota Fiscal',
               'Modalidade', 'Nº Requisição', 'Movimento', 'Produto', 'Quantidade',
               'saldo')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response


@login_required
def render_to_pdf(template_src, context_dic={}):
    template = get_template(template_src)
    html = template.render(context_dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
