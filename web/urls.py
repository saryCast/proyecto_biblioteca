from django.urls import path
from . import views
from .views import index, CustomLoginView, CustomLogoutView, RegisterView, agregarLibro, arrendar, misArriendos,retornar,devolver

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accountlogout/', CustomLogoutView.as_view(), name='logout'),
    path('libros/', agregarLibro, name='crearLib'),
    path('libros/<int:id>/arrendar/', arrendar, name='arrendar'),

    path('arriendos/', misArriendos, name='mis_arriendos'),
    path('libros/<int:id>/retornar/', retornar, name='retornar'),
    path('arriendos/<int:id>/devolver', devolver, name='devolver'),


]