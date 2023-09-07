from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login, logout
from .models import TpUsuario

# Create your views here.
def index(request):
    return render(request, 'rtdf/index.html')

##Registro de usuario


def registro(request):
    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)

        if registro_form.is_valid():
            usuario = registro_form.save(commit=False)
            usuario.set_password(usuario.password)
            
            tipo_usuario = registro_form.cleaned_data['tipo_usuario']
            usuario.id_tp_usuario = tipo_usuario

            usuario.save()

            return redirect('login')

    else:
        registro_form = RegistroForm(initial={'tipo_usuario': TpUsuario.objects.get(pk=2)})

    return render(request, 'registro/registro.html', {'registro_form': registro_form})

##Login para el usuario

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, 'registro/login.html', {'error_message': error_message})

    return render(request, 'registro/login.html')

##Cierre de sesion

def logout_view(request):
    logout(request)
    return redirect('index')  