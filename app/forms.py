from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Livro

class LivrosForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(LivrosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'titulo',
            'autor',
            'editora',
            'genero',
            'preco',
            'data_pub',
            'status',
            Submit('submit', 'Salvar')
        )

class FazerReservaForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Seu Nome")
    email = forms.EmailField(label="Seu E-mail")
    cpf = forms.CharField(max_length=11, label="Seu CPF")