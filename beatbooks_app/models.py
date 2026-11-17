from django.db import models
from django.contrib.auth.models import User

CORES_AVATAR = [
    ('#1CB0F6', 'Azul BeatBooks'),
    ('#58CC02', 'Verde Conquista'),
    ('#FF8600', 'Laranja Solar'),
    ('#CE82FF', 'Roxo Épico'),
    ('#FF4B4B', 'Coral Vibrante'),
    ('#00CD9C', 'Menta Fresco'),
]

OPCOES_AVALIACAO = [
    ('OTIMO', 'Ótimo ⭐⭐⭐⭐⭐'),
    ('BOM', 'Bom ⭐⭐⭐⭐'),
    ('MEDIO', 'Médio ⭐⭐⭐'),
    ('RUIM', 'Ruim ⭐⭐'),
    ('DETESTEI', 'Detestei ⭐'),
]

class PerfilLeitor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nome_exibicao = models.CharField(max_length=100)
    arroba = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    cor_avatar = models.CharField(max_length=20, choices=CORES_AVATAR, default='#1CB0F6')
    inscrito_acesso_antecipado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Perfil de Leitor'
        verbose_name_plural = 'Perfis de Leitores'

    def __str__(self):
        return f"{self.nome_exibicao} ({self.arroba})"

    @property
    def iniciais(self):
        partes = self.nome_exibicao.strip().split()
        if len(partes) >= 2:
            return (partes[0][0] + partes[1][0]).upper()
        if len(partes) == 1 and len(partes[0]) > 0:
            return partes[0][:2].upper()
        return "BB"


class LivroLido(models.Model):
    perfil = models.ForeignKey(PerfilLeitor, on_delete=models.CASCADE, related_name='livros')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros_lidos')
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField(blank=True, null=True)
    total_paginas = models.IntegerField(blank=True, null=True)
    avaliacao = models.CharField(max_length=15, choices=OPCOES_AVALIACAO, blank=True, null=True)
    resumo = models.TextField()
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Livro Lido'
        verbose_name_plural = 'Livros Lidos'
        ordering = ['-data_adicionado']

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
