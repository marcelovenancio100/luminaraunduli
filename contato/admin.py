from django.contrib import admin
from .models import Categoria, Contato


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_filter = ('nome',)
    search_fields = ('nome',)
    list_per_page = 10


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email', 'telefone', 'categoria', 'data_criacao', 'mostrar')
    list_display_links = ('nome',)
    list_filter = ('nome', 'sobrenome')
    search_fields = ('nome', 'sobrenome', 'email', 'telefone')
    list_per_page = 10
    list_editable = ('telefone', 'mostrar')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Contato, ContatoAdmin)
