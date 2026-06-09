from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Cidade)
admin.site.register(Autor)
admin.site.register(Editora)
admin.site.register(Leitor)
admin.site.register(Livro)
admin.site.register(Genero)