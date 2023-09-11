from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login, logout
from .models import TpUsuario, Usuario, RelacionPaPro, ProfesionalSalud, Paciente
from django.http import HttpResponseForbidden

# Create your views here.
def index(request):
    tipo_usuario = None 
    usuarios = Usuario.objects.all()
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'rtdf/index.html', {'tipo_usuario': tipo_usuario, 'usuario': usuarios})

##ESTE APARTADO SOLO SERA PARA MODIFICAR LOS BOTONES DEL NAV

def base(request):
    tipo_usuario = None 

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'rtdf/base.html', {'tipo_usuario': tipo_usuario})


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

##LISTADO DE LOS PACIENTES

def listado_pacientes(request):

    tipo_usuario = None 
    usuarios = Usuario.objects.all()
    # se verifica que el usuario este registrado como profesional salud
    if request.user.groups.filter(name='ProfesionalesSalud').exists() or request.user.has_perm('nombre_permiso'):
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        #se obtiene el identificador del fonoaudiologo
        profesional_salud = request.user.profesionalsalud

        # se filtra los pacientes vinculados
        pacientes_relacionados = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        # lista de pacientes con datos de usuario y paciente
        pacientes = []

        for relacion in pacientes_relacionados:
            paciente_dict = {
                'id_paciente': relacion.id_paciente.id_paciente,
                'primer_nombre': relacion.id_paciente.id_usuario.primer_nombre,
                'ap_paterno': relacion.id_paciente.id_usuario.ap_paterno,
                'email': relacion.id_paciente.id_usuario.email,
                'numero_telefonico': relacion.id_paciente.id_usuario.numero_telefonico,
                'telegram': relacion.id_paciente.telegram,
                'fecha_nacimiento': relacion.id_paciente.id_usuario.fecha_nacimiento,
                'tipo_diabetes': relacion.id_paciente.fk_tipo_diabetes,
                'tipo_hipertension': relacion.id_paciente.fk_tipo_hipertension,
            }
            pacientes.append(paciente_dict)

        return render(request, 'rtdf/listado_pacientes.html', {'tipo_usuario': tipo_usuario, 'usuario': usuarios, 'pacientes': pacientes})
    else:
        return HttpResponseForbidden("De momento se debe configurar el usuario como profesional de salud directamente desde el administrador de django")


def vocalizacion(request):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request,'rtdf/vocalizacion.html', {'tipo_usuario': tipo_usuario})

def intensidad(request):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request,'rtdf/intensidad.html', {'tipo_usuario': tipo_usuario})

##Cierre de sesion

def logout_view(request):
    logout(request)
    return redirect('index')  

##LISTADO DE LOS PACIENTES PARA ADMINSITRADOR

def list_paci_admin(request):
    pacientes = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Paciente')
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/list_paci_admin.html',{'tipo_usuario': tipo_usuario, 'pacientes': pacientes})


##LISTADO DE LOS FONOAUDIOLOGOS PARA ADMINSITRADOR

def list_fono_admin(request):

    fonoaudiologo_list = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Fonoaudiologo')
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/list_fono_admin.html',{'tipo_usuario': tipo_usuario, 'fonoaudiologo_list':fonoaudiologo_list})

##Cierre de sesion