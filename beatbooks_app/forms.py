from django import forms
from django.contrib.auth.models import User
from .models import PerfilLeitor, LivroLido

class CadastroForm(forms.ModelForm):
    nome_exibicao = forms.CharField(
        max_length=100,
        label="Nome de Exibição",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Maria Clara', 'class': 'input-beatbooks'})
    )
    arroba = forms.CharField(
        max_length=50,
        label="Seu @ de Leitor",
        widget=forms.TextInput(attrs={'placeholder': '@mariaclara', 'class': 'input-beatbooks'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha segura', 'class': 'input-beatbooks'})
    )
    confirmacao_senha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha', 'class': 'input-beatbooks'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Nome de Usuário (Login)',
            'email': 'E-mail para Acesso Antecipado',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'usuario123', 'class': 'input-beatbooks'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seuemail@exemplo.com', 'class': 'input-beatbooks'}),
        }

    def clean_arroba(self):
        arroba = self.cleaned_data.get('arroba', '').strip()
        if not arroba.startswith('@'):
            arroba = f"@{arroba}"
        return arroba

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmacao_senha = cleaned_data.get('confirmacao_senha')
        if senha and confirmacao_senha and senha != confirmacao_senha:
            self.add_error('confirmacao_senha', 'As senhas informadas não coincidem.')
        return cleaned_data


class PerfilLeitorForm(forms.ModelForm):
    class Meta:
        model = PerfilLeitor
        fields = ['nome_exibicao', 'arroba', 'bio', 'cor_avatar']
        labels = {
            'nome_exibicao': 'Nome de Exibição',
            'arroba': 'Identificador (@)',
            'bio': 'Sua Bio de Leitor',
            'cor_avatar': 'Cor do seu Avatar',
        }
        widgets = {
            'nome_exibicao': forms.TextInput(attrs={'placeholder': 'Ex: Carlos Drummond', 'class': 'input-beatbooks'}),
            'arroba': forms.TextInput(attrs={'placeholder': '@carlos.leitor', 'class': 'input-beatbooks'}),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Conte sobre seus gêneros favoritos, autores prediletos ou seus hábitos de leitura...',
                'class': 'input-beatbooks textarea-beatbooks',
                'rows': 4
            }),
            'cor_avatar': forms.Select(attrs={'class': 'input-beatbooks select-beatbooks'}),
        }

    def clean_arroba(self):
        arroba = self.cleaned_data.get('arroba', '').strip()
        if not arroba.startswith('@'):
            arroba = f"@{arroba}"
        return arroba


class LivroLidoForm(forms.ModelForm):
    class Meta:
        model = LivroLido
        fields = ['titulo', 'autor', 'ano_publicacao', 'total_paginas', 'avaliacao', 'resumo']
        labels = {
            'titulo': 'Título do Livro',
            'autor': 'Autor(a)',
            'ano_publicacao': 'Ano de Publicação (Opcional)',
            'total_paginas': 'Total de Páginas (Opcional)',
            'avaliacao': 'O que achou desta leitura?',
            'resumo': 'Seu Pequeno Resumo sobre o Livro',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Grande Sertão: Veredas', 'class': 'input-beatbooks'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Ex: João Guimarães Rosa', 'class': 'input-beatbooks'}),
            'ano_publicacao': forms.NumberInput(attrs={'placeholder': 'Ex: 1956', 'class': 'input-beatbooks'}),
            'total_paginas': forms.NumberInput(attrs={'placeholder': 'Ex: 600', 'class': 'input-beatbooks'}),
            'avaliacao': forms.Select(attrs={'class': 'input-beatbooks select-beatbooks'}),
            'resumo': forms.Textarea(attrs={
                'placeholder': 'Escreva em poucas linhas suas impressões, os pontos mais marcantes e o que você aprendeu com esta leitura...',
                'class': 'input-beatbooks textarea-beatbooks',
                'rows': 5
            }),
        }

