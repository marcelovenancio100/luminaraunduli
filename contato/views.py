from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    # contatos = Contato.objects.all()
    # contatos = Contato.objects.order_by('nome')
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )

    paginator = Paginator(contatos, 10)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contato/index.html', {
        'contatos': contatos
    })


def pesquisar(request):
    filter = request.GET.get('filter')

    if filter is None or not filter:
        # raise Http404()
        messages.add_message(request, messages.ERROR, 'Digite um filtro para pesquisar ...')
        return redirect('index')

    fields = Concat('nome', Value(' '), 'sobrenome')

    # contatos = Contato.objects.order_by('-id').filter(
    #     Q(nome__icontains=filter) | Q(sobrenome__icontains=filter),
    #     mostrar=True
    # )

    contatos = Contato.objects.annotate(
        nome_completo=fields
    ).filter(
        Q(nome_completo__icontains=filter) | Q(telefone__icontains=filter),
        mostrar=True
    )

    print(contatos.query)
    paginator = Paginator(contatos, 10)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contato/pesquisar.html', {
        'contatos': contatos
    })


def detail(request, id):
    # contato = Contato.objects.get(id=id)
    contato = get_object_or_404(Contato, id=id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contato/detail.html', {
        'contato': contato
    })
