from django.shortcuts import render,redirect,get_object_or_404
from  django.views import View
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from web.models import *
from .forms import CategoriaForm, LibroForm

# Create your views here.
@login_required
def index(request):
    form=CategoriaForm(request.GET)
    if form.is_valid():
        categoria=form.cleaned_data.get('categoria')

        if categoria:
            libros=Libro.objects.filter(categoria=categoria)
        else:
            libros=Libro.objects.all().filter(arrendador__isnull=True)
    else:
        libros=Libro.objects.all()

    return render(request,'index.html',{'libros':libros,'form':form})


class RegisterView(View):
    def get(self, request):
        return render(request,'registration/register.html')
    
    def post(self, request):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2:
            messages.error(request,'passwords do not match')
            return redirect(reverse('register'))
        user=User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name)
         #user.is_active = False
        user.save()
        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('index')
    
class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Sesion Iniciada Exitosamente"
    template_name = 'registration/login.html'  
    redirect_authenticated_user = True
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, "Sesion Cerrada Exitosamente")
        return response

@login_required
def agregarLibro(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para agregar libros.")
        return redirect('index')
    
    if request.method=='POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = LibroForm()
    
    return render(request, 'crearLibro.html', {'form': form})

@login_required
def arrendar(request, id):
    libro = get_object_or_404(Libro, id=id)

    if request.method == 'POST':
    
        fecha = request.POST.get('fecha')
        fecha_seleccionada = timezone.datetime.strptime(fecha, "%Y-%m-%d").date()
        fecha_hoy = timezone.now().date()
        
        if fecha_seleccionada < fecha_hoy:
            messages.error(request, "La fecha seleccionada debe ser hoy o una fecha futura.")
            return render(request, 'arrendar.html', {'libro': libro})
       
        nuevo_arriendo = Arriendo.objects.create(fecha_arriendo=fecha, user=request.user, libro=libro)

        libro.arrendador = request.user
        libro.save()
        
        return redirect('index')  
    return render(request, 'arrendar.html', {'libro':libro})

@login_required
def misArriendos(request):
    arriendos = Arriendo.objects.filter(user=request.user, fecha_retorno__isnull=True)
    print(arriendos)
    return render(request,'mis_arriendos.html',{'arriendos':arriendos})

@login_required
def retornar(request,id):
    arriendo=get_object_or_404(Arriendo, id=id)
    return render(request,'retornar.html',{'arriendo':arriendo})    

@login_required
def devolver(request, id):
    arriendo = get_object_or_404(Arriendo, id=id)
    print(arriendo)
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        fecha_seleccionada = timezone.datetime.strptime(fecha, "%Y-%m-%d").date()

        if fecha_seleccionada <= arriendo.fecha_arriendo:
            messages.error(request, "La fecha seleccionada debe ser superior a la fecha de arriendo")
            return render(request, 'retornar.html', {'arriendo': arriendo})

        dias_retraso = (fecha_seleccionada - arriendo.fecha_arriendo).days - arriendo.libro.tipo.dias_arriendo
        if  dias_retraso>0:
            deuda=dias_retraso*arriendo.libro.tipo.precio_dias_atraso
        else:
            deuda=0
            dias_retraso = 0

        arriendo.fecha_retorno=fecha_seleccionada
        arriendo.multa = deuda
        arriendo.save()
        libro=arriendo.libro
        libro.arrendador=None
        libro.save()
        

        if deuda > 0:
            messages.success(request, f"El libro {arriendo.libro.nombre} se retornó con {dias_retraso} días de retraso, generando ${deuda} en multa.")
        else:
            messages.success(request, f"El libro {arriendo.libro.nombre} se retornó sin retraso.")

        return redirect('mis_arriendos')

    return render(request, 'retornar.html', {'arriendo': arriendo})