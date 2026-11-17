from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resumos/', views.resumos_comunidade, name='resumos_comunidade'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('livro/novo/', views.adicionar_livro, name='adicionar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro, name='editar_livro'),
    path('livro/<int:livro_id>/excluir/', views.excluir_livro, name='excluir_livro'),
]

