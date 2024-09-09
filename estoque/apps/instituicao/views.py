from datetime import datetime
from io import BytesIO
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
from estoque.apps.instituicao.actions.export_xlsx import export_xlsx
from estoque.apps.instituicao.actions.import_xlsx import (
    import_xlsx as action_import_xlsx
)
from .models import Instituicao
from .forms import InstituicaoFormAdmin


class InstituicaoList(ListView):
    model = Instituicao
    template_name = 'instituicao_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(instituicao__icontains=search)
                |Q(inep__icontains=search)
            )
        return qs


@login_required
def instituicao_detail(request, pk):
    template_name = 'instituicao_detail.html'
    obj = Instituicao.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


class InstituicaoCreate(CreateView):
    form_class = InstituicaoFormAdmin
    template_name = 'instituicao_form.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            "Instituição Adicionada com Sucesso!"
        )
        return super(InstituicaoCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro! Verifique se todos os campos estão preenchidos!"
        )
        return super(InstituicaoCreate, self).form_invalid(form)


class InstituicaoUpdate(UpdateView):
    model = Instituicao
    fields = ('__all__')
    template_name = 'instituicao_form.html'


class InstituicaoDelete(DeleteView):
    model = Instituicao
    template_name = 'instituicao_confirm_delete.html'
    success_url = reverse_lazy('instituicao:instituicao_list')


@login_required
def import_xlsx(request):
    filename = 'fix/instituicoes.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Intituições Importadas com Sucesso!')
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(reverse('instituicao:instituicao_list'))


@login_required
def exportar_instituicoes_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Instituicao'
    filename = 'instituicoes_exportadas.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Instituicao.objects.all().values_list(
        'instituicao',
        'denominacao',
        'inep',
        'diretora',
        'telefone',
        'email',
    )
    columns = ('Instituição', 'Denominação', 'INEP', 'Diretor(a)', 'Telefone',
               'E-mail')
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


def ViewPDFDetail(request, *args, **kwargs):
    pk = kwargs.get('pk')
    instituicao = get_object_or_404(Instituicao, pk=pk)

    template_path = 'instituicao_pdf.html'
    context = {
        'object': instituicao
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="instituicao_pdf.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros <pre>' + html + '</pre>')
    return response
