from django.contrib import admin
from .models import PerfilLeitor, LivroLido

@admin.register(PerfilLeitor)
class PerfilLeitorAdmin(admin.ModelAdmin):
    list_display = ('nome_exibicao', 'arroba', 'usuario', 'cor_avatar', 'inscrito_acesso_antecipado')
    search_fields = ('nome_exibicao', 'arroba', 'usuario__username', 'bio')
    list_filter = ('inscrito_acesso_antecipado', 'cor_avatar')

@admin.register(LivroLido)
class LivroLidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'perfil', 'ano_publicacao', 'total_paginas', 'avaliacao', 'data_adicionado')
    search_fields = ('titulo', 'autor', 'resumo', 'perfil__nome_exibicao', 'perfil__arroba')
    list_filter = ('avaliacao', 'data_adicionado')
