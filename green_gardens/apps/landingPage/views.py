from django.shortcuts import render, get_object_or_404, redirect
from .models import ElementoImagem, ConfigSite, Secao, Avaliacao, Ebook
from django.http import HttpResponse
from .forms import ContatoForm, EbookForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.http import FileResponse
import os

# --------------------------> inicio das funções/classes auxiliares <-------------------------------------------

def get_context(name_session):
    """

    """
    secao = get_object_or_404(Secao, titulo=name_session)
    imgs = ElementoImagem.objects.filter(secao=secao)
    return secao, imgs

def get_context_latest(name_session, limit_number):
    """
    
    """
    secao = get_object_or_404(Secao, titulo=name_session)
    imgs = ElementoImagem.objects.filter(secao=secao).order_by('-id')[:limit_number]
    return secao, imgs

# --------------------------> final das funções/classes auxiliares <-------------------------------------------

def index(request):
    """
        
    """
    # obtendo os nomes das seções
    all_secoes = Secao.objects.all()
    nomes_secoes = [name.titulo for name in all_secoes]

    print(nomes_secoes)

    # configurações do site
    config_site = ConfigSite.objects.latest('id')

    # Seção 0 : banner pricipal
    ## obtendo as imagens do banner principal
    _, imgs_banner_principal = get_context(nomes_secoes[0])[:5]

    # Seção 1 : sobre
    secao_sobre = Secao.objects.get(titulo=nomes_secoes[1])

    # Seção 2 : Nossos serviços
    secao_nossos_servicos, imgs_nossos_servicos = get_context_latest(nomes_secoes[2],2)

    # Seção Nossos serviços para o mobile
    _, imgs_nossos_servicos_mobile = get_context_latest(nomes_secoes[2],5)

    # seção 3 : ebook 
    try:
        secao_ebook = Secao.objects.get(titulo=nomes_secoes[3])
    except Secao.DoesNotExist:
        secao_ebook = None

    # ebook principal - o que será visualizado na landing page
    try:
        ebook_principal = Ebook.objects.latest('id')
    except Ebook.DoesNotExist:
        ebook_principal = None

    # Seção 4 : valores
    secao_valores, imgs_valores = get_context(nomes_secoes[4])

    # Seção 5 : avaliação
    ## Obtendo a ultima avaliacao
    try:
        last_avaliacao = Avaliacao.objects.latest('id')
    except Avaliacao.DoesNotExist:
        last_avaliacao = None
    
    secao_avaliacao = Secao.objects.filter(titulo=nomes_secoes[5])
    if last_avaliacao is not None:
        img_avaliacao = ElementoImagem.objects.filter(secao=secao_avaliacao).get()
    else:
        img_avaliacao = None

    # Seção 6 : galeria
    secao_galeria, img_galeria = get_context(nomes_secoes[6])

    if request.method == "POST":

        # parte de tratamento do forms de contato e envio de email personalizado
        if 'contato_form' in request.POST:    
            form_ebook = EbookForm()
            form_contato = ContatoForm(request.POST)
            if form_contato.is_valid():
                assunto = "Pedido de Contato"
                email_from = settings.EMAIL_HOST_USER
                destinatario = [form_contato.cleaned_data['email']]

                html_content = render_to_string('emails/confirm.html', {
                    "nome": form_contato.cleaned_data['nome'],
                    "telefone": form_contato.cleaned_data['telefone'],
                    "mensagem": form_contato.cleaned_data['mensagem'],
                })

                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(assunto, text_content, email_from, destinatario)
                email.attach_alternative(html_content, 'text/html')
                email.send()
                messages.success(request, "email enviado com sucesso!")
            else:
                messages.error(request, "erro no envio do email!")

        # parte de tratamento do forms para download do ebook
        if 'ebook_form' in request.POST:
            form_contato = ContatoForm()
            form_ebook = EbookForm(request.POST)
            if form_ebook.is_valid():
                file_path = os.path.join(settings.MEDIA_ROOT, ebook_principal.conteudo.name)
                messages.success(request, "ebook baixado com sucesso!")
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=ebook_principal.conteudo.name)
            else:
                messages.error(request, "erro no download!")
    else:
        form_contato = ContatoForm()
        form_ebook = EbookForm()

    return render(request, 'index.html', {
       'imgs_banner_principal': imgs_banner_principal,
       'sobre': secao_sobre,
       'secao_nossos_servicos': secao_nossos_servicos,
       'imgs_nossos_servicos': imgs_nossos_servicos,
       'imgs_nossos_servicos_mobile': imgs_nossos_servicos_mobile,
       'secao_valores': secao_valores,
       'imgs_valores': imgs_valores,
       'avaliacao': last_avaliacao,
       'secao_galeria': secao_galeria,
       'imgs_galeria': img_galeria,
       'config_site': config_site,
       'form_contato': form_contato,
       'img_avaliacao': img_avaliacao,
       'secao_ebook': secao_ebook,
       'ebook_principal': ebook_principal,
       'form_ebook': form_ebook,
    })

def dynamic_css_view(request):
    style_config = ConfigSite.objects.first()
    context = {
        'cor_primaria': style_config.cor_primaria,
        'cor_secundaria': style_config.cor_secundaria,
    }
    response = render(request, 'styles/dynamic_styles.css', context, content_type='text/css')
    return HttpResponse(response)