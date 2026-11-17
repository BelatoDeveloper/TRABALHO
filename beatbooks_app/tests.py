from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PerfilLeitor, LivroLido

class BeatBooksTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='mariademo', password='password123', email='maria@teste.com')
        self.perfil = PerfilLeitor.objects.create(
            usuario=self.user,
            nome_exibicao='Maria Teste',
            arroba='@maria.teste',
            bio='Leitora apaixonada.',
            cor_avatar='#1CB0F6',
            inscrito_acesso_antecipado=True
        )
        self.livro = LivroLido.objects.create(
            perfil=self.perfil,
            usuario=self.user,
            titulo='Capitães da Areia',
            autor='Jorge Amado',
            ano_publicacao=1937,
            total_paginas=280,
            avaliacao='OTIMO',
            resumo='Um retrato cru e poético dos meninos marginalizados de Salvador.'
        )

    def test_home_page_acessivel_anonimo(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BeatBooks')
        self.assertContains(response, 'Capitães da Areia')

    def test_perfil_requer_login(self):
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_adicionar_livro_requer_login(self):
        response = self.client.get(reverse('adicionar_livro'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_perfil_logado(self):
        self.client.login(username='mariademo', password='password123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Teste')
        self.assertContains(response, '@maria.teste')
        self.assertContains(response, 'Capitães da Areia')

    def test_cadastro_cria_usuario_e_perfil(self):
        response = self.client.post(reverse('cadastro'), {
            'username': 'novoleitor',
            'nome_exibicao': 'Novo Leitor',
            'arroba': 'novoleitor',
            'email': 'novo@teste.com',
            'senha': 'novasenha123',
            'confirmacao_senha': 'novasenha123'
        })
        self.assertEqual(response.status_code, 302)
        user_criado = User.objects.get(username='novoleitor')
        self.assertIsNotNone(user_criado)
        self.assertEqual(user_criado.perfil.nome_exibicao, 'Novo Leitor')
        self.assertEqual(user_criado.perfil.arroba, '@novoleitor')
        self.assertTrue(user_criado.perfil.inscrito_acesso_antecipado)

    def test_adicionar_e_excluir_livro(self):
        self.client.login(username='mariademo', password='password123')
        resp_add = self.client.post(reverse('adicionar_livro'), {
            'titulo': 'Vidas Secas',
            'autor': 'Graciliano Ramos',
            'ano_publicacao': 1938,
            'total_paginas': 176,
            'avaliacao': 'OTIMO',
            'resumo': 'Narrativa cortante sobre a aridez do sertão e a desumanização da família de Fabiano.'
        })
        self.assertEqual(resp_add.status_code, 302)
        self.assertTrue(LivroLido.objects.filter(titulo='Vidas Secas').exists())

        livro_criado = LivroLido.objects.get(titulo='Vidas Secas')
        resp_del = self.client.post(reverse('excluir_livro', args=[livro_criado.id]))
        self.assertEqual(resp_del.status_code, 302)
        self.assertFalse(LivroLido.objects.filter(titulo='Vidas Secas').exists())
