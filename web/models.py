from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre = models.CharField(max_length=50)
    dias_arriendo = models.IntegerField()
    precio_dias_atraso = models.IntegerField()

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    nombre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=45)
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    arrendador = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Arriendo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_arriendo = models.DateField()
    fecha_retorno = models.DateField(null=True, blank=True)
    multa = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.libro.nombre}'