from django.shortcuts import render
from .models import ElementoImagem, ConfigSite, Secao, Avaliacao
from django.http import HttpResponse

def index(request):
    # configurações do site
    config_site = ConfigSite.objects.latest('id')

    # Seção do banner pricipal
    secao_banner_principal = Secao.objects.get(titulo="Banner Principal")
    imgs_banner_principal = ElementoImagem.objects.filter(secao=secao_banner_principal)

    # Seção sobre
    secao_sobre = Secao.objects.get(titulo="Sobre")

    # Seção Nossos serviços
    secao_nossos_servicos = Secao.objects.get(titulo="Nossos Serviços")
    imgs_nossos_servicos = ElementoImagem.objects.filter(secao=secao_nossos_servicos)

    # Seção valores
    secao_valores = Secao.objects.get(titulo="Valores")
    imgs_valores = ElementoImagem.objects.filter(secao=secao_valores)

    # Obtendo a ultima avaliacao
    last_avaliacao = Avaliacao.objects.latest('id')

    # Seção galeria
    secao_galeria = Secao.objects.get(titulo="Galeria")
    img_galeria = ElementoImagem.objects.filter(secao=secao_galeria)

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
    })

def dynamic_css_view(request):
    style_config = ConfigSite.objects.first()
    context = {
        'cor_primaria': style_config.cor_primaria,
        'cor_secundaria': style_config.cor_secundaria,
    }
    response = render(request, 'styles/dynamic_styles.css', context, content_type='text/css')
    return HttpResponse(response)