import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beatbooks_project.settings')
django.setup()

from django.contrib.auth.models import User
from beatbooks_app.models import PerfilLeitor, LivroLido

if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@beatbooks.com', 'admin123')
    PerfilLeitor.objects.create(
        usuario=admin_user,
        nome_exibicao='Administrador BeatBooks',
        arroba='@admin.beatbooks',
        bio='Curador oficial da plataforma e explorador de grandes narrativas.',
        cor_avatar='#1CB0F6',
        inscrito_acesso_antecipado=True
    )
    print("Superusuário 'admin' criado com senha 'admin123'.")

demo_user, created = User.objects.get_or_create(
    username='eduardo.demo',
    defaults={'email': 'eduardo@beatbooks.com'}
)
if created:
    demo_user.set_password('demo123')
    demo_user.save()

perfil_demo, _ = PerfilLeitor.objects.get_or_create(
    usuario=demo_user,
    defaults={
        'nome_exibicao': 'Eduardo Santos',
        'arroba': '@eduardo.leitor',
        'bio': 'Apaixonado por ficção clássica, realismo fantástico e memórias literárias. Leitor voraz nas madrugadas.',
        'cor_avatar': '#58CC02',
        'inscrito_acesso_antecipado': True
    }
)

livros_iniciais = [
    {
        'titulo': 'Dom Casmurro',
        'autor': 'Machado de Assis',
        'ano_publicacao': 1899,
        'total_paginas': 256,
        'avaliacao': 'OTIMO',
        'resumo': 'A genialidade machadiana brilha em cada linha da narrativa de Bento Santiago. A dúvida sobre Capitu é apenas a superfície de um estudo psicológico profundo sobre ciúme, memória e a fragilidade das certezas humanas.'
    },
    {
        'titulo': 'A Metamorfose',
        'autor': 'Franz Kafka',
        'ano_publicacao': 1915,
        'total_paginas': 96,
        'avaliacao': 'OTIMO',
        'resumo': 'Gregor Samsa acorda transformado em inseto, mas a verdadeira tragédia é como sua família e o trabalho o descartam imediatamente quando ele perde sua utilidade econômica. Uma obra atemporal e arrebatadora.'
    },
    {
        'titulo': 'O Pequeno Príncipe',
        'autor': 'Antoine de Saint-Exupéry',
        'ano_publicacao': 1943,
        'total_paginas': 120,
        'avaliacao': 'OTIMO',
        'resumo': 'Uma fábula poética sobre o valor do que é invisível aos olhos. A relação com a rosa e a raposa traz lições essenciais sobre responsabilidade afetiva e ternura em um mundo apressado.'
    }
]

for dados in livros_iniciais:
    if not LivroLido.objects.filter(titulo=dados['titulo'], usuario=demo_user).exists():
        LivroLido.objects.create(
            perfil=perfil_demo,
            usuario=demo_user,
            **dados
        )
        print(f"Livro '{dados['titulo']}' adicionado.")

print("Dados iniciais configurados com sucesso!")
