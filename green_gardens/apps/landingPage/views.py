from django.shortcuts import render, get_object_or_404, redirect
from .models import ElementoImagem, ConfigSite, Secao, Avaliacao, Ebook
from .forms import ContatoForm, UsuarioForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.http import FileResponse
import os
from django.http import JsonResponse

# --------------------------> inicio das funções/classes auxiliares <-------------------------------------------

def get_context(name_session):
    """
      Funcão generica para obter todas as  instancias do modelo ElementoImagem
      
      args:
        - name_session: nome da seção ao qual se quer obter as instancias
        
      return:
        - secao: instacia do modelo secao com o titulo = name_session
        - imgs: todas as instancias do modelo ElementoImagem que estão relacionadas com a secao
    """
    secao = get_object_or_404(Secao, titulo=name_session)
    imgs = ElementoImagem.objects.filter(secao=secao)
    return secao, imgs

def get_context_latest(name_session, limit_number):
    """
      funcao para se obter um numero especifico das ultimas instancias do modelo ElementoImagem
      
      args:
        - name_session: nome da seção ao qual se quer obter as instancias
        - imgs: Ultimas (limit_number) instancias do modelo ElementoImagem
    """
    secao = get_object_or_404(Secao, titulo=name_session)
    imgs = ElementoImagem.objects.filter(secao=secao).order_by('-id')[:limit_number]
    return secao, imgs

# --------------------------> final das funções/classes auxiliares <-------------------------------------------

def index(request):
    """
      view principal para tratamento dos dados dos formularios e obtenção dos contextos da landing page
    """
    # obtendo os nomes das seções
    try: 
        all_secoes = Secao.objects.all()
    except Secao.DoesNotExist:
        all_secoes = None
    
    if all_secoes is not None:
        nomes_secoes = [name.titulo for name in all_secoes]
    else:
        nomes_secoes = None


    # configurações do site
    try:
        config_site = ConfigSite.objects.latest('id')
    except ConfigSite.DoesNotExist:
        config_site = None

    # Seção 0 : banner pricipal
    ## obtendo as imagens do banner principal
    if nomes_secoes != []:
        secao_banner_principal, imgs_banner_principal = get_context(nomes_secoes[0])[:5]
    else:
        secao_banner_principal, imgs_banner_principal = None, None
    try:
        pre_load_img_banner = ElementoImagem.objects.filter(secao=secao_banner_principal).first()
    except ElementoImagem.DoesNotExist:
        pre_load_img_banner = None


    # Seção 1 : sobre
    try:
        secao_sobre, img_secao_sobre = get_context(nomes_secoes[1])
        img_secao_sobre = img_secao_sobre.get()
    except:
        secao_sobre, img_secao_sobre = None, None

    
    # Seção 2 : Nossos serviços
    try:
        secao_nossos_servicos, imgs_nossos_servicos = get_context_latest(nomes_secoes[2],2)
        ## Seção 2 : Nossos serviços para o mobile
        _, imgs_nossos_servicos_mobile = get_context_latest(nomes_secoes[2],5)
    except:
        secao_nossos_servicos, imgs_nossos_servicos,imgs_nossos_servicos_mobile = None, None, None 

    
    # Seção 3 : ebook 
    if nomes_secoes != []:
        secao_ebook = Secao.objects.get(titulo=nomes_secoes[3])
        ## ebook principal - o que será visualizado na landing page
        try:
            ebook_principal = Ebook.objects.latest('id')
        except Ebook.DoesNotExist:
            ebook_principal = None
    else:
        secao_ebook, ebook_principal = None, None

    
    # Seção 4 : valores
    if nomes_secoes != []:
        secao_valores, imgs_valores = get_context(nomes_secoes[4])
    else:
        secao_valores, imgs_valores = None, None

    
    # Seção 5 : avaliação
    ## Obtendo a ultima avaliacao
    try:
        last_avaliacao = Avaliacao.objects.latest('id')
    except Avaliacao.DoesNotExist:
        last_avaliacao = None

    if nomes_secoes != []:
        secao_avaliacao = Secao.objects.filter(titulo=nomes_secoes[5]).get()
    else:
        secao_avaliacao = None
    if last_avaliacao is not None:
        img_avaliacao = ElementoImagem.objects.filter(secao=secao_avaliacao).last()
    else:
        img_avaliacao = None


    # Seção 6 : galeria
    if nomes_secoes != []:  
        secao_galeria, img_galeria = get_context(nomes_secoes[6])
    else:
        secao_galeria, img_galeria = None, None

    form_contato = ContatoForm()
    form_ebook = UsuarioForm()

    
    # tratamento dos formularios - contato e ebook
    if request.method == "POST":
        # parte de tratamento do forms de contato e envio de email personalizado
        if 'contato_form' in request.POST:
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
                return redirect('landingPage:index')

    return render(request, 'index.html', {
       'imgs_banner_principal': imgs_banner_principal,
       'preload_img_banner': pre_load_img_banner,
       'sobre': secao_sobre,
       'img_sobre': img_secao_sobre,
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

def download_ebook(request):
    """
        View para realizar o download do ebook

        return: retorna uma resposta que contem o arquivo do ebook
    """
    ebook_principal = Ebook.objects.latest('id')
    file_path = os.path.join(settings.MEDIA_ROOT, ebook_principal.conteudo.name)
    if request.method == 'POST':
        
        form_ebook = UsuarioForm(request.POST)
        if form_ebook.is_valid():
            form_ebook.save()
            data = {
                'sucess': True,
                'url_download': reverse('landingPage:download-ebook'),
            }
            return JsonResponse(data)
        else:
            print("erro")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=ebook_principal.conteudo.name)


    
