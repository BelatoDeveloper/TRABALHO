from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilLeitor, LivroLido
from .forms import CadastroForm, PerfilLeitorForm, LivroLidoForm

LIMITE_VITRINE_HOME = 6

def home(request):
    resumos_recentes = LivroLido.objects.select_related('perfil', 'usuario').all()[:LIMITE_VITRINE_HOME]
    total_inscritos = PerfilLeitor.objects.filter(inscrito_acesso_antecipado=True).count()
    total_livros = LivroLido.objects.count()
    context = {
        'resumos_recentes': resumos_recentes,
        'total_inscritos': total_inscritos,
        'total_livros': total_livros,
    }
    return render(request, 'home.html', context)

def resumos_comunidade(request):
    resumos = LivroLido.objects.select_related('perfil', 'usuario').all()
    return render(request, 'comunidade.html', {'resumos': resumos})

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()

            PerfilLeitor.objects.create(
                usuario=user,
                nome_exibicao=form.cleaned_data['nome_exibicao'],
                arroba=form.cleaned_data['arroba'],
                inscrito_acesso_antecipado=True
            )

            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Você foi inscrito no Acesso Antecipado do BeatBooks.')
            return redirect('perfil')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bem-vindo(a) de volta, {usuario.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('perfil')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
        if 'next' in request.GET:
            messages.info(request, 'Acesso restrito: faça login com sua conta para acessar seu Perfil e gerenciar seus resumos.')

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta com sucesso.')
    return redirect('home')

@login_required(login_url='login')
def perfil(request):
    perfil_usuario, _ = PerfilLeitor.objects.get_or_create(
        usuario=request.user,
        defaults={
            'nome_exibicao': request.user.first_name or request.user.username,
            'arroba': f'@{request.user.username}',
            'inscrito_acesso_antecipado': True,
        }
    )
    livros_usuario = LivroLido.objects.filter(usuario=request.user)
    context = {
        'perfil': perfil_usuario,
        'livros': livros_usuario,
        'total_meus_livros': livros_usuario.count(),
    }
    return render(request, 'perfil.html', context)

@login_required(login_url='login')
def editar_perfil(request):
    perfil_usuario, _ = PerfilLeitor.objects.get_or_create(
        usuario=request.user,
        defaults={
            'nome_exibicao': request.user.first_name or request.user.username,
            'arroba': f'@{request.user.username}',
            'inscrito_acesso_antecipado': True,
        }
    )

    if request.method == 'POST':
        form = PerfilLeitorForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilLeitorForm(instance=perfil_usuario)

    return render(request, 'editar_perfil.html', {'form': form, 'perfil': perfil_usuario})

@login_required(login_url='login')
def adicionar_livro(request):
    perfil_usuario, _ = PerfilLeitor.objects.get_or_create(
        usuario=request.user,
        defaults={
            'nome_exibicao': request.user.username,
            'arroba': f'@{request.user.username}',
        }
    )

    if request.method == 'POST':
        form = LivroLidoForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.perfil = perfil_usuario
            livro.usuario = request.user
            livro.save()
            messages.success(request, f'O livro "{livro.titulo}" e seu resumo foram adicionados à sua estante!')
            return redirect('perfil')
    else:
        form = LivroLidoForm()

    return render(request, 'form_livro.html', {
        'form': form,
        'acao': 'Adicionar Livro Lido',
        'subtitulo': 'Cadastre um livro concluído e eternize suas memórias e impressões sobre a obra.'
    })

@login_required(login_url='login')
def editar_livro(request, livro_id):
    livro = get_object_or_404(LivroLido, id=livro_id, usuario=request.user)

    if request.method == 'POST':
        form = LivroLidoForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, f'O livro "{livro.titulo}" foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = LivroLidoForm(instance=livro)

    return render(request, 'form_livro.html', {
        'form': form,
        'livro': livro,
        'acao': 'Editar Livro e Resumo',
        'subtitulo': f'Atualize as informações e o resumo de "{livro.titulo}".'
    })

@login_required(login_url='login')
def excluir_livro(request, livro_id):
    livro = get_object_or_404(LivroLido, id=livro_id, usuario=request.user)

    if request.method == 'POST':
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f'O livro "{titulo}" foi removido da sua estante.')
        return redirect('perfil')

    return render(request, 'confirmar_exclusao.html', {'livro': livro})
