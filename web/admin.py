from django.contrib import admin
from .models import Categoria, Arriendo, Tipo, Libro

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Arriendo)
admin.site.register(Tipo)

class LibroAdmin(admin.ModelAdmin):
    list_display=('nombre','categoria','tipo')

admin.site.register(Libro,LibroAdmin)