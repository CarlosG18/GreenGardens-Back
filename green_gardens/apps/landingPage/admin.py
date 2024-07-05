from django.contrib import admin
from .models import ElementoImagem

@admin.register(ElementoImagem)
class ElementoCarroselsConfig(admin.ModelAdmin):
    list_filter = ["secao"]
