from django.shortcuts import render
from .models import ElementoImagem



# Create your views here.
def index(request):
    imgs_banner_principal = ElementoImagem.objects.filter(secao="banner_principal")
    imgs_nossos_servicos = ElementoImagem.objects.filter(secao="nossos_serviços")
    return render(request, 'index.html', {
        'imgs': imgs_banner_principal,
        'imgs_nossos_servicos': imgs_nossos_servicos,
        'mensagem': "teste",
    })