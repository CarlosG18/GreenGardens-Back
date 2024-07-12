from django.contrib import admin
from .models import ElementoImagem, ConfigSite, Secao, Avaliacao, Ebook, Usuario
from django.core.exceptions import ValidationError

class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permite adicionar uma nova instância apenas se não houver nenhuma
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if self.model.objects.count() >= 1:
            extra_context['show_message'] = True
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if self.model.objects.count() >= 1:
            instance = self.model.objects.first()
            extra_context['show_message'] = True
            extra_context['instance'] = instance
        return super().changelist_view(request, extra_context)
    
@admin.register(ConfigSite)
class ConfiguracaoAdmin(SingletonModelAdmin):
    fieldsets = [
        ("configurações meta", {'fields': ('linguagem','descricao_site', 'title', 'cor_primaria', 'cor_secundaria')}),
        ("contato", {'fields': ('endereco', 'email' ,'maps', 'telefone')}),
        ("links", {'fields': ('link_insta', 'link_face')}),
    ]

@admin.register(ElementoImagem)
class ElementoCarroselsConfig(admin.ModelAdmin):
    list_filter = ["secao"]

@admin.register(Secao)
class SecaoConfig(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Retorna False se houver 6 ou mais instâncias de Secao
        if Secao.objects.count() >= 7:
            return False
        return super().has_add_permission(request)
    
admin.site.register(Avaliacao)
admin.site.register(Ebook)
admin.site.register(Usuario)






