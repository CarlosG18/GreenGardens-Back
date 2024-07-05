from django.shortcuts import render, get_object_or_404, redirect
from .models import ElementoImagem, ConfigSite, Secao, Avaliacao
from django.http import HttpResponse
from .forms import ContatoForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def get_context(name_session):
    secao = get_object_or_404(Secao, titulo=name_session)
    imgs = ElementoImagem.objects.filter(secao=secao)
    return secao, imgs

def index(request):
    # configurações do site
    config_site = ConfigSite.objects.latest('id')

    # Seção do banner pricipal
    _, imgs_banner_principal = get_context("Banner Principal")

    # Seção sobre
    secao_sobre = Secao.objects.get(titulo="Sobre")

    # Seção Nossos serviços
    secao_nossos_servicos, imgs_nossos_servicos = get_context("Nossos Serviços")

    # Seção valores
    secao_valores, imgs_valores = get_context("Valores")
    
    # Obtendo a ultima avaliacao
    last_avaliacao = Avaliacao.objects.latest('id')

    # Seção galeria
    secao_galeria, img_galeria = get_context("Galeria")

    # parte de tratamento do forms de contato e envio de email personalizado
    if request.method == "POST":
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
            return redirect('landingPage:index')

    else:
        form_contato = ContatoForm()

    return render(request, 'index.html', {
       'imgs_banner_principal': imgs_banner_principal,
       'sobre': secao_sobre,
       'secao_nossos_servicos': secao_nossos_servicos,
       'imgs_nossos_servicos': imgs_nossos_servicos,
       'secao_valores': secao_valores,
       'imgs_valores': imgs_valores,
       'avaliacao': last_avaliacao,
       'secao_galeria': secao_galeria,
       'imgs_galeria': img_galeria,
       'config_site': config_site,
       'form_contato': form_contato,
    })

def dynamic_css_view(request):
    style_config = ConfigSite.objects.first()
    context = {
        'cor_primaria': style_config.cor_primaria,
        'cor_secundaria': style_config.cor_secundaria,
    }
    response = render(request, 'styles/dynamic_styles.css', context, content_type='text/css')
    return HttpResponse(response)