from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Requisicao
from .forms import RequisicaoFormAdmin


class RequisicaoList(ListView):
    model = Requisicao
    template_name = 'requisicao_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(requisicao__icontains=search)
                |Q(instituicao__instituicao__icontains=search)
                |Q(data__icontains=search)
            )
        return qs


class RequisicaoCreate(CreateView):
    form_class = RequisicaoFormAdmin
    template_name = 'requisicao_form.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            "Requisição Adicionada com Sucesso!"
        )
        return super(RequisicaoCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro! Verifique se todos os campos estão preenchidos!"
        )
        return super(RequisicaoCreate, self).form_invalid(form)


class RequisicaoUpdate(UpdateView):
    model = Requisicao
    fields = ('__all__')
    template_name = 'requisicao_form.html'


class RequisicaoDelete(DeleteView):
    model = Requisicao
    template_name = 'requisicao_confirm_delete.html'
    success_url = reverse_lazy('requisicao:requisicao_list')
