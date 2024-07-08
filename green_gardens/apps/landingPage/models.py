from django.db import models
from django.core.validators import RegexValidator
import os

# --------------------------> funções/classes auxiliares <-------------------------------------------

def dinamic_path(instance, filename):
    return os.path.join("img/"+instance.secao.path, filename)

def path_ebook(instance, filename):
    return os.path.join("ebook/"+instance.assunto, filename)

def path_img_ebook(instance, filename):
    return os.path.join("img/ebook/"+instance.assunto, filename)

# ----------------------------> Modelos <------------------------------------------------------------

class Secao(models.Model):
    class Meta:
        verbose_name = "seções"
        verbose_name_plural = "seções"
    
    titulo = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=200, blank=False, editable=False, null=False, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z0-9_]+$'
        )
    ])
    descricao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.titulo:
            self.path = self.titulo.lower().replace(' ', '_')
        super(Secao, self).save(*args, **kwargs)

    def __str__(self):
        return f'seção {self.titulo}'

class ConfigSite(models.Model):
    """
        modelo para dinamizar algumas configuraçoes da landing page (inclui links do footer, titulo do site, linguagem, contatos)
    """

    class Meta:
        verbose_name = "Configurações da landing page"
        verbose_name_plural = "Configurações da landing page"

    CHOICES_LINGUAGEM = [
        ("en","en"),
        ("pt-br","pt-br"),
    ]

    descricao_site = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    linguagem = models.CharField(max_length=10, blank=False, null=False, choices=CHOICES_LINGUAGEM,default="en")
    cor_primaria = models.CharField(max_length=7, default="#000000")
    cor_secundaria = models.CharField(max_length=7, default="#000000")
    endereco = models.CharField(max_length=300,blank=False, null=False, default='')
    maps = models.CharField(max_length=500,blank=False, null=False,default='')
    email = models.CharField(max_length=300,blank=False, null=False, default='')
    telefone = models.CharField(max_length=100,blank=False, null=False, default='')
    link_insta = models.CharField(max_length=100,blank=False, null=False, default='')
    link_face = models.CharField(max_length=100,blank=False, null=False, default='')


    def __str__(self):
        return f'configurações da landing page'

class ElementoImagem(models.Model):
    """
        Modelo para dinamização de todas as imagens presentes na landing page
            - Elemento: definido como a imagem em si, a seção ao qual ela está relacionada, titulo, descrição e texto alternativo (alt)
    """

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"

    titulo = models.CharField(max_length=200,blank=True, null=True)
    secao = models.ForeignKey(Secao, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200, blank=True, null=True)
    img = models.ImageField(upload_to=dinamic_path,blank=False, null=False)
    alt_img = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        if self.titulo:
            return f'img - {self.titulo} - seção - {self.secao}'
        else:
            return f'img - {self.id} - seção - {self.secao}'
    
class Avaliacao(models.Model):
    """
        modelo para dinamizar as avaliações do site
    """

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    comentario = models.TextField(blank=False, null=False)
    autor = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return f'avaliação da(o) {self.autor}'
    
class Ebook(models.Model):
    """
        modelo para dinamizar os ebook que serão disponiveis para download
    """

    titulo = models.CharField(max_length=200, blank=False, null=False)
    assunto = models.CharField(max_length=200, blank=False, null=False)
    conteudo = models.FileField(upload_to=path_ebook, blank=False, null=False)
    img_capa = models.ImageField(upload_to=path_img_ebook,blank=False, null=False)

    def __str__(self):
        return f'ebook - {self.titulo}'
