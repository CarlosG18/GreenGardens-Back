from django.db import models

class ElementoImagem(models.Model):
    """
        Modelo para dinamização de todas as imagens presentes na landing page
            - Elemento: definido como a imagem em si, a seção ao qual ela está relacionada, titulo, descrição e texto alternativo (alt)
    """
    CHOICES_SECAO = [
        ("banner_principal","banner_principal"),
        ("sobre","sobre"),
        ("nossos_serviços","nossos_serviços"),
        ("infoprodutos","infoprodutos"),
        ("valores","valores"),
        ("galeria","galeria"),
    ]

    titulo = models.CharField(max_length=200,blank=True, null=True)
    secao = models.CharField(max_length=100, choices=CHOICES_SECAO,blank=False, null=False)
    descricao = models.CharField(max_length=200, blank=True, null=True)
    alt = models.CharField(max_length=200,blank=True,null=True)
    img = models.ImageField(upload_to='img/',blank=False, null=False)

    def __str__(self):
        return f'img - {self.titulo} - seção - {self.secao}'