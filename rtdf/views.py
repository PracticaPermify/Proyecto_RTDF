from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
@login_required
def index(request):
    return render(request, 'rtdf/index.html')

from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)

        if registro_form.is_valid():
            usuario = registro_form.save(commit=False)
            usuario.set_password(usuario.password)
            usuario.save()

            # Puedes agregar más lógica aquí, como redireccionar al usuario a una página de inicio de sesión.

            return redirect('login')

    else:
        registro_form = RegistroForm()

    return render(request, 'registro/registro.html', {'registro_form': registro_form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            # Redireccionar a la página de inicio o a donde desees después del inicio de sesión
            return redirect('index')
        else:
            # Mostrar un mensaje de error de inicio de sesión
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, 'registro/login.html', {'error_message': error_message})

    return render(request, 'registro/login.html')
