from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from .forms import LivrosForm
from .forms import FazerReservaForm
from django.utils import timezone

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        livros = Livro.objects.all()
        return render(request, 'index.html', {'livros': livros})
    def post(self, request):
        pass

class LivrosView(View):
    def get(self, request, *args, **kwargs):
        livros = Livro.objects.all()
        return render(request, 'livros.html', {'livros': livros})

class EmprestimoView(View):
    def get(self, request, *args, **kwargs):
        reservas = Emprestimo.objects.all().select_related('livro', 'leitor')
        return render(request, 'reserva.html', {'reservas': reservas})

class CidadesView(View):
    def get(self, request, *args, **kwargs):
        cidades = Cidade.objects.all()
        return render(request, 'cidade.html', {'cidades': cidades})

class AutoresView(View):
    def get(self, request, *args, **kwargs):
        autores = Autor.objects.all()
        return render(request, 'autor.html', {'autores': autores})

class EditorasView(View):
    def get(self, request, *args, **kwargs):
        editoras = Editora.objects.all()
        return render(request, 'editora.html', {'editoras': editoras})

class LeitoresView(View):
    def get(self, request, *args, **kwargs):
        leitores = Leitor.objects.all()
        return render(request, 'leitor.html', {'leitores': leitores})

class GenerosView(View):
    def get(self, request, *args, **kwargs):
        generos = Genero.objects.all()
        return render(request, 'genero.html', {'generos': generos})

class DeleteLivroView(View):
    def get(self, request, id, *args, **kwargs):
        livro = Livro.objects.get(id=id)
        livro.delete()
        messages.success(request, 'Livro deletado com sucesso!')
        return redirect('livros')
    
class EditarLivroView(View):
    template_name = 'editar_livro.html'

    def get(self, request, id, *args, **kwargs):
        livro = get_object_or_404(Livro, id=id)
        form = LivrosForm(instance=livro)
        return render(request, self.template_name, {'livro': livro, 'form': form})

    def post(self, request, id, *args, **kwargs):
        livro = get_object_or_404(Livro, id=id)
        form = LivrosForm(request.POST, instance=livro)

        if form.is_valid():
            form.save()
            messages.success(request, 'As edições foram salvas com sucesso.')
            return redirect('editar', id=id)
        else:
            messages.error(request, 'Corrija os erros no formulário antes de enviar novamente.')

        return render(request, self.template_name, {'livro': livro, 'form': form})
    
class FazerReservaView(View):
    template_name = 'fazer_reserva.html'

    def get(self, request, livro_id):
        livro = get_object_or_404(Livro, id=livro_id)
        form = FazerReservaForm()
        return render(request, self.template_name, {'livro': livro, 'form': form})

    def post(self, request, livro_id):
        livro = get_object_or_404(Livro, id=livro_id)
        form = FazerReservaForm(request.POST)

        if form.is_valid():
            # Pega ou cria o leitor baseado no CPF digitado para não duplicar
            leitor, created = Leitor.objects.get_or_create(
                cpf=form.cleaned_data['cpf'],
                defaults={
                    'nome': form.cleaned_data['nome'],
                    'email': form.cleaned_data['email']
                }
            )
            
            # Cria o registro da reserva na tabela Emprestimo
            Emprestimo.objects.create(
                livro=livro,
                leitor=leitor,
                data_emprestimo=timezone.now().date()
            )
            
            messages.success(request, f'Livro "{livro.nome}" reservado com sucesso!')
            return redirect('reserva') # Redireciona para a página de reservas
            
        return render(request, self.template_name, {'livro': livro, 'form': form})
    
class CancelarReservaView(View):
    def get(self, request, *args, **kwargs):
        reserva_id = next(iter(kwargs.values()))
        
        reserva = get_object_or_404(Emprestimo, id=reserva_id)
        nome_livro = reserva.livro.nome
        reserva.delete()
        
        messages.success(request, f'Reserva do livro "{nome_livro}" cancelada com sucesso!')
        return redirect('reserva')