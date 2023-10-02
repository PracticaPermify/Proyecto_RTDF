from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def validate(request):
    if request.is_anonymous:
        print(request)
        return False
    elif request:
        print(request)
        return True

def index(request):
    tipo_usuario = None 
    usuarios = Usuario.objects.all()

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    usuarios_por_pagina = 10  # Número de usuarios por página

    paginator = Paginator(usuarios, usuarios_por_pagina)  # Crea un objeto Paginator

    # Obtiene el número de página actual desde la solicitud GET
    page_number = request.GET.get('page')

    # Obtiene la página actual de usuarios
    page = paginator.get_page(page_number)

    return render(request, 'rtdf/index.html', {'tipo_usuario': tipo_usuario, 
                                               'usuario': page})  # Pasamos la página en lugar de usuarios

##ESTE APARTADO SOLO SERA PARA MODIFICAR LOS BOTONES DEL NAV

def base(request):
    tipo_usuario = None 

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'rtdf/base.html', {'tipo_usuario': tipo_usuario})

def registro(request):
    regiones = Region.objects.all()
    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)

        if registro_form.is_valid():
            usuario = registro_form.save(commit=False)
            usuario.set_password(usuario.password)

            tipo_usuario = registro_form.cleaned_data['tipo_usuario']
            usuario.id_tp_usuario = tipo_usuario
            usuario.save()
            
            if tipo_usuario.tipo_usuario == 'Paciente':
                paciente = Paciente(
                    telegram=registro_form.cleaned_data['telegram'],
                    fk_tipo_hipertension=registro_form.cleaned_data['fk_tipo_hipertension'],
                    fk_tipo_diabetes=registro_form.cleaned_data['fk_tipo_diabetes'],
                    id_usuario=usuario
                )
                paciente.save()

            elif tipo_usuario.tipo_usuario == 'Familiar':
                rut_paciente = registro_form.cleaned_data.get('rut_paciente')

                # Verificar si el RUT del paciente existe en la base de datos
                try:
                    paciente_relacionado = Paciente.objects.get(id_usuario__numero_identificacion=rut_paciente)
                except Paciente.DoesNotExist:
                    mensaje_error = 'El paciente con el RUT proporcionado no se encuentra en la base de datos.'
                    return render(request, 'registro/registro.html', {'registro_form': registro_form, 
                                                                      'regiones': regiones,
                                                                      'mensaje_error': mensaje_error})

                familiar = FamiliarPaciente(
                    fk_tipo_familiar=registro_form.cleaned_data['fk_tipo_familiar'],
                    id_usuario=usuario
                )
                familiar.save()

                relacion_fp = RelacionFp(
                    id_paciente=paciente_relacionado,
                    fk_familiar_paciente=familiar
                )
                relacion_fp.save()

            return redirect('login')

    else:
        registro_form = RegistroForm()

    return render(request, 'registro/registro.html', {'registro_form': registro_form, 
                                                      'regiones': regiones})

def obtener_provincias(request):
    region_id = request.GET.get('region_id')
    provincias = Provincia.objects.filter(id_region=region_id).values('id_provincia', 'provincia')
    return JsonResponse(list(provincias), safe=False)

def obtener_comunas(request):
    provincia_id = request.GET.get('provincia_id')
    comunas = Comuna.objects.filter(id_provincia=provincia_id).values('id_comuna', 'comuna')
    return JsonResponse(list(comunas), safe=False)

##Login para el usuario

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            response = redirect('index')
            response.set_cookie('logged_in', 'true')
            return response
        else:
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, 'registro/login.html', {'error_message': error_message})
    else:
        response = render(request, 'registro/login.html')

    response['Cache-Control'] = 'no-store'

    return response

##Cierre de sesion

def logout_view(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('logged_in')  # Elimina la cookie de inicio de sesión
    return response

##LISTADO DE LOS PACIENTES------------------------------------------

##LISTADO DE LOS PACIENTES FONOAUDIOLOGOS------------------------------------------

##LISTADO DE LOS PACIENTES FONOAUDIOLOGOS------------------------------------------

@user_passes_test(validate)
def listado_pacientes(request):

    tipo_usuario = None 
    usuarios = Usuario.objects.all()

    # se verifica que el usuario este registrado como profesional salud
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # se obtiene el identificador de la fk usuario relacionado al fonoaudiologo
        id_usuario = request.user.id_usuario

        try:
            # se obtiene el fonoaudiologo relacionado
            profesional_salud = ProfesionalSalud.objects.get(id_usuario=id_usuario)
        except ProfesionalSalud.DoesNotExist:
            profesional_salud = None

        # lista para almacenar los pacientes relacionados
        pacientes_relacionados = []

        # filtrado de los pacientes relacionados
        if profesional_salud:
            pacientes_relacionados = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        # lista de los pacientes con datos de usuario y paciente
        pacientes = []

        # se cargan los datos en variables 
        for relacion in pacientes_relacionados:
            paciente_dicc = {
                'id_usuario': relacion.id_paciente.id_usuario.id_usuario,
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
            pacientes.append(paciente_dicc)

    return render(request, 'vista_profe/listado_pacientes.html', {'tipo_usuario': tipo_usuario, 
                                                                  'usuario': usuarios, 
                                                                  'pacientes': pacientes,})

##Detalles por paciente de los fonoaudiologos
@user_passes_test(validate)
def detalle_prof_paci(request, paciente_id):

    paciente = get_object_or_404(Usuario, id_usuario=paciente_id, id_tp_usuario__tipo_usuario='Paciente')
    traer_paciente = paciente.paciente

    obtener_rasati = Rasati.objects.filter(id_informe__fk_relacion_pa_pro__id_paciente=traer_paciente)
    obtener_grbas = Grbas.objects.filter(id_informe__fk_relacion_pa_pro__id_paciente=traer_paciente)

    informes_rasati = obtener_rasati 
    informes_grbas = obtener_grbas    

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    paciente = get_object_or_404(Usuario, id_usuario=paciente_id, id_tp_usuario__tipo_usuario='Paciente')
    paciente_info = paciente.paciente

    fonoaudiologos_asociados = ProfesionalSalud.objects.filter(relacionpapro__id_paciente=paciente_info.id_paciente)

    return render(request, 'vista_profe/detalle_prof_paci.html', {'paciente': paciente, 
                                                                 'tipo_usuario': tipo_usuario,
                                                                 'paciente_info': paciente_info,
                                                                 'fonoaudiologos_asociados': fonoaudiologos_asociados,
                                                                 'informes_rasati': informes_rasati,
                                                                 'informes_grbas': informes_grbas,
                                                                 })

def listado_informes(request):
    # Obtén el fonoaudiólogo actual
    profesional_medico = request.user.profesionalsalud

    # Filtra los informes asociados al fonoaudiólogo actual
    informes = Informe.objects.filter(fk_relacion_pa_pro__fk_profesional_salud=profesional_medico).annotate(
    num_pautas_terapeuticas=Count('pautaterapeutica')).order_by('-fecha')

    informes_por_pagina = 10

    paginator = Paginator(informes, informes_por_pagina)

    # Obtiene el número de página actual desde la solicitud GET
    page_number = request.GET.get('page')

    # Obtiene la página actual de informes
    page = paginator.get_page(page_number)

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'vista_profe/listado_informes.html', {'informes': informes,
                                                                 'tipo_usuario': tipo_usuario,
                                                                 'page': page})
    

@user_passes_test(validate)
def detalle_prof_infor(request, informe_id):

    source = request.GET.get('source')

    if source == 'plantilla1':
        url_regreso = reverse('detalle_prof_paci')
    elif source == 'plantilla2':
        url_regreso = reverse('listado_informes')
    else:
        # Si no proviene de ninguna de las plantillas conocidas, configura una URL predeterminada
        url_regreso = reverse('listado_informes')

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    informe = get_object_or_404(Informe, id_informe=informe_id)

    try:
        grbas = Grbas.objects.get(id_informe=informe)
    except Grbas.DoesNotExist:
        grbas = None

    try:
        rasati = Rasati.objects.get(id_informe=informe)
    except Rasati.DoesNotExist:
        rasati = None

    datos_vocalizacion = Vocalizacion.objects.filter(id_pauta_terapeutica__fk_informe=informe_id,id_pauta_terapeutica__fk_tp_terapia= 1)    
    datos_intensidad = Intensidad.objects.filter(id_pauta_terapeutica__fk_informe=informe_id,id_pauta_terapeutica__fk_tp_terapia= 2)

    # Obtén el paciente relacionado con este informe
    paciente_relacionado = informe.fk_relacion_pa_pro.id_paciente

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        if request.method == 'POST':

            #guardo la pk del informe del detalle_informe
            informe = Informe.objects.get(pk=informe_id)
            form = PautaTerapeuticaForm(request.POST)
            vocalizacion_form = VocalizacionForm(request.POST)
            intensidad_form = IntensidadForm(request.POST)

            if form.is_valid() and vocalizacion_form.is_valid() and intensidad_form.is_valid():
                pauta_terapeutica = form.save(commit=False) #guardo el form para agregar el id informe manualmente
                pauta_terapeutica.fk_informe = informe # le paso la pk del informe
                pauta_terapeutica.save()

                tipo_terapia = str(form.cleaned_data['fk_tp_terapia']).strip()

                # Asociar el informe con GRBAS y RASATI
                if tipo_terapia == 'Vocalización':
                    
                    vocalizacion = vocalizacion_form.save(commit=False)
                    vocalizacion.id_pauta_terapeutica = pauta_terapeutica
                    vocalizacion.save()

                elif tipo_terapia == 'Intensidad':

                    intensidad = intensidad_form.save(commit=False)
                    intensidad.id_pauta_terapeutica = pauta_terapeutica
                    intensidad.save()    

                return redirect('detalle_prof_infor', informe_id=informe.id_informe)
        

        else:
            # Si la solicitud no es POST, muestra el formulario en blanco
            form = PautaTerapeuticaForm()
            vocalizacion_form = VocalizacionForm()
            intensidad_form = IntensidadForm()

        return render(request, 'vista_profe/detalle_prof_infor.html', {
            'form': form,
            'vocalizacion_form': vocalizacion_form,
            'intensidad_form': intensidad_form,
            'datos_intensidad': datos_intensidad,
            'informe': informe,
            'datos_vocalizacion': datos_vocalizacion,
            'grbas': grbas,
            'rasati': rasati,
            'paciente_relacionado': paciente_relacionado,
            'tipo_usuario': tipo_usuario,
            'url_regreso': url_regreso,
        })
    
    else:
        return redirect('vista_profe/index.html')
    
##Listado para los familiares--------------------------------------

@user_passes_test(validate)
def lista_familiar(request):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # se obtiene el identificador de la fk usuario relacionado al fonoaudiologo
        id_usuario = request.user.id_usuario

        try:
            # se obtiene el fonoaudiologo relacionado
            familiar = FamiliarPaciente.objects.get(id_usuario=id_usuario)
        except FamiliarPaciente.DoesNotExist:
            familiar = None

        # lista para almacenar los pacientes relacionados
        pacientes_relacionados = []

        # filtrado de los pacientes relacionados
        if familiar:
            pacientes_relacionados = RelacionFp.objects.filter(fk_familiar_paciente=familiar)

        # lista de los pacientes con datos de usuario y paciente
        pacientes = []

        # se cargan los datos en variables 
        for relacion in pacientes_relacionados:
            paciente_dicc = {
                'id_usuario': relacion.id_paciente.id_usuario.id_usuario,
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
            pacientes.append(paciente_dicc)

    return render(request,'vista_familiar/lista_familiar.html', {'tipo_usuario': tipo_usuario, 'pacientes': pacientes})

## Detalles de los pacientes de un familiar

@user_passes_test(validate)
def detalle_familiar(request, paciente_id):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    paciente = get_object_or_404(Usuario, id_usuario=paciente_id, id_tp_usuario__tipo_usuario='Paciente')
    paciente_info = paciente.paciente

    fonoaudiologos_asociados = ProfesionalSalud.objects.filter(relacionpapro__id_paciente=paciente_info.id_paciente)

    return render(request, 'vista_familiar/detalle_familiar.html',{'paciente': paciente, 
                                                                 'tipo_usuario': tipo_usuario,
                                                                 'paciente_info': paciente_info,
                                                                 'fonoaudiologos_asociados': fonoaudiologos_asociados
                                                                 })

##Ejercicios de vocalización-----------------------------------

@user_passes_test(validate)
def vocalizacion(request):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request,'vista_paciente/vocalizacion.html', {'tipo_usuario': tipo_usuario})

@user_passes_test(validate)
def intensidad(request):

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request,'vista_paciente/intensidad.html', {'tipo_usuario': tipo_usuario})

@user_passes_test(validate)
def mi_fonoaudiologo(request):

    tipo_usuario = None 
    usuarios = Usuario.objects.all()

    # se verifica que el usuario este registrado como profesional salud
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # se obtiene el identificador de la fk usuario relacionado al fonoaudiologo
        id_usuario = request.user.id_usuario #Paciente Ricardo Rodriguez Tobalaba su ID de usuario es 9

        try:
            # se obtiene el fonoaudiologo relacionado
            paciente_salud = Paciente.objects.get(id_usuario=id_usuario)# Mi id de usuario se compara con profesional salud...No
        except Paciente.DoesNotExist:
            paciente_salud = None

        # lista para almacenar los pacientes relacionados
        profesional_relacionados = []

        # filtrado de los pacientes relacionados
        if paciente_salud:
            profesional_relacionados = RelacionPaPro.objects.filter(id_paciente=paciente_salud)

        # lista de los pacientes con datos de usuario y paciente
        pacientes = []

        # se cargan los datos en variables 
        for relacion in profesional_relacionados:
            paciente_dicc = {
                'id_fonoaudiologo': relacion.fk_profesional_salud.id_profesional_salud,
                'id_usuario_fonoaudiologo':relacion.fk_profesional_salud.id_usuario.id_usuario,
                'nombre_profesional_salud':relacion.fk_profesional_salud.id_usuario.primer_nombre,
                'ap_paterno_profesional_salud':relacion.fk_profesional_salud.id_usuario.ap_paterno,
                'correo_profesional_salud':relacion.fk_profesional_salud.id_usuario.email,
                'numero_telefonico_profesional_salud':relacion.fk_profesional_salud.id_usuario.numero_telefonico,
                #'id_paciente': relacion.id_paciente.id_paciente,
                #'primer_nombre': relacion.id_paciente.id_usuario.primer_nombre,
                #'ap_paterno': relacion.id_paciente.id_usuario.ap_paterno,
                #'email': relacion.id_paciente.id_usuario.email,
                #'numero_telefonico': relacion.id_paciente.id_usuario.numero_telefonico,
                #'telegram': relacion.id_paciente.telegram,
                #'fecha_nacimiento': relacion.id_paciente.id_usuario.fecha_nacimiento,
                #'tipo_diabetes': relacion.id_paciente.fk_tipo_diabetes,
                #'tipo_hipertension': relacion.id_paciente.fk_tipo_hipertension,
            }
            pacientes.append(paciente_dicc)

    return render(request, 'vista_paciente/mi_fonoaudiologo.html', {'tipo_usuario': tipo_usuario, 'usuario': usuarios, 'pacientes': pacientes})


##LISTADO DE LOS PACIENTES PARA ADMINSITRADOR

@user_passes_test(validate)
def list_paci_admin(request):
    pacientes = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Paciente')
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/list_paci_admin.html',{'tipo_usuario': tipo_usuario, 'pacientes': pacientes})

@user_passes_test(validate)
def detalle_paciente(request, paciente_id):
    paciente = get_object_or_404(Usuario, id_usuario=paciente_id, id_tp_usuario__tipo_usuario='Paciente')
    traer_paciente = paciente.paciente

    fonoaudiologos_asociados = ProfesionalSalud.objects.filter(relacionpapro__id_paciente=traer_paciente.id_paciente)

    obtener_rasati = Rasati.objects.filter(id_informe__fk_relacion_pa_pro__id_paciente=traer_paciente)
    obtener_grbas = Grbas.objects.filter(id_informe__fk_relacion_pa_pro__id_paciente=traer_paciente)

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    informes_rasati = obtener_rasati 
    informes_grbas = obtener_grbas    

    return render(request, 'vista_admin/detalle_paciente.html', {
        'paciente': paciente,
        'tipo_usuario': tipo_usuario,
        'paciente_info': traer_paciente,
        'fonoaudiologos_asociados': fonoaudiologos_asociados,
        'informes_rasati': informes_rasati,
        'informes_grbas': informes_grbas,
    })

##LISTADO DE LOS FONOAUDIOLOGOS PARA ADMINSITRADOR

@user_passes_test(validate)
def list_fono_admin(request):
    fonoaudiologos = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Fonoaudiologo')
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/list_fono_admin.html', {'tipo_usuario': tipo_usuario, 'fonoaudiologos': fonoaudiologos})

@user_passes_test(validate)
def detalle_fonoaudiologo(request, fonoaudiologo_id):

    fonoaudiologo = get_object_or_404(Usuario, id_usuario=fonoaudiologo_id, id_tp_usuario__tipo_usuario='Fonoaudiólogo')

    profesional_salud = ProfesionalSalud.objects.get(id_usuario=fonoaudiologo)

    institucion = ProfesionalSalud.objects.get(id_usuario=fonoaudiologo).id_institucion

    relaciones = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

    pacientes_asociados = [relacion.id_paciente for relacion in relaciones]

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/detalle_fonoaudiologo.html', {'fonoaudiologo': fonoaudiologo, 
                                                                      'tipo_usuario': tipo_usuario,
                                                                      'pacientes_asociados': pacientes_asociados,
                                                                      'profesional_salud': profesional_salud,
                                                                      'institucion': institucion})

##LISTADO PARA NEUROLOGOS PARA ADMINSITRADOR

@user_passes_test(validate)
def list_neur_admin(request):
    neurologos = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Neurologo')
    
    tipo_usuario = None 
    usuarios = Usuario.objects.all()
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'vista_admin/list_neur_admin.html', {'tipo_usuario': tipo_usuario, 
                                                                'usuario': usuarios,
                                                                'neurologos': neurologos})

@user_passes_test(validate)
def detalle_neurologo(request, neurologo_id):

    neurologo = get_object_or_404(Usuario, id_usuario=neurologo_id, id_tp_usuario__tipo_usuario='Neurologo')

    profesional_salud = ProfesionalSalud.objects.get(id_usuario=neurologo)

    institucion = ProfesionalSalud.objects.get(id_usuario=neurologo).id_institucion

    relaciones = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

    pacientes_asociados = [relacion.id_paciente for relacion in relaciones]


    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
    return render(request, 'vista_admin/detalle_neurologo.html', {  'neurologo': neurologo, 
                                                                    'tipo_usuario': tipo_usuario,
                                                                    'pacientes_asociados': pacientes_asociados,
                                                                    'profesional_salud': profesional_salud,
                                                                    'institucion': institucion})

##LISTADO PARA FAMILIARES PARA VISTA DE ADMINISTRADOR

@user_passes_test(validate)
def list_fami_admin(request):
    familiar = Usuario.objects.filter(id_tp_usuario__tipo_usuario='Familiar')
    
    tipo_usuario = None 
    usuarios = Usuario.objects.all()
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'vista_admin/list_fami_admin.html', {'tipo_usuario': tipo_usuario, 
                                                                'usuario': usuarios,
                                                                'familiar': familiar})

@user_passes_test(validate)
def detalle_familiar_admin(request, familiar_id):
    familiar = get_object_or_404(Usuario, id_usuario=familiar_id, id_tp_usuario__tipo_usuario='Familiar')

    familiar_paciente = FamiliarPaciente.objects.get(id_usuario=familiar)
    parentesco = familiar_paciente.fk_tipo_familiar

    relacion_fp = RelacionFp.objects.filter(fk_familiar_paciente=familiar_paciente).first()
    paciente_asociado = relacion_fp.id_paciente if relacion_fp else None


    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    return render(request, 'vista_admin/detalle_familiar_admin.html', {
                                                                'familiar': familiar, 
                                                                'tipo_usuario': tipo_usuario,
                                                                'parentesco': parentesco,
                                                                'paciente_asociado': paciente_asociado
                                                            })
##Ayuda pancho

@user_passes_test(validate)
def ingresar_informes(request):
    tipo_usuario = None

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
        
        profesional_salud = request.user.profesionalsalud
        relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        if request.method == 'POST':
            form = InformeForm(request.POST)
            grbas_form = GrbasForm(request.POST)
            rasati_form = RasatiForm(request.POST)

            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes

            if form.is_valid() and grbas_form.is_valid() and rasati_form.is_valid():
                informe = form.save()
                tipo_informe = str(form.cleaned_data['tp_informe']).strip()
                informe.fecha = timezone.now()
                print(f"Tipo de informe seleccionado: {tipo_informe}")

                # Asociar el informe con GRBAS y RASATI
                if tipo_informe == 'GRBAS':
                    
                    grbas = grbas_form.save(commit=False)
                    grbas.id_informe = informe
                    grbas.save()

                elif tipo_informe == 'RASATI':
                    
                    ##print(f"Tipo AAA: {tipo_informe}")    
                    rasati = rasati_form.save(commit=False)
                    rasati.id_informe = informe
                    rasati.save()

                return redirect('listado_informes')
        else:
            form = InformeForm(initial={'fecha': timezone.now()})
            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes
            grbas_form = GrbasForm()
            rasati_form = RasatiForm()
            

        return render(request, 'vista_profe/ingresar_informes.html', {
            'form': form,
            'grbas_form': grbas_form,
            'rasati_form': rasati_form,
            'tipo_usuario': tipo_usuario,
        })
    else:
        return redirect('vista_profe/index.html')
    


def editar_informe(request, informe_id):
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        informe = get_object_or_404(Informe, id_informe=informe_id)
        profesional_salud = request.user.profesionalsalud
        relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        rasati_form = None
        grbas_form = None

        try:
            if informe.rasati:
                rasati_form = RasatiForm(request.POST or None, instance=informe.rasati)
        except Rasati.DoesNotExist:
            rasati_form = RasatiForm()

        try:
            if informe.grbas:
                grbas_form = GrbasForm(request.POST or None, instance=informe.grbas)
        except Grbas.DoesNotExist:
            grbas_form = GrbasForm()

        if request.method == 'POST':
            form = InformeForm(request.POST, instance=informe)
            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes

            if form.is_valid():
                informe.fecha = timezone.now()
                form.save()

            if rasati_form and rasati_form.is_valid():
                rasati_form.save()

            if grbas_form and grbas_form.is_valid():
                grbas_form.save()

            return redirect('detalle_prof_infor', informe_id=informe.id_informe)
        else:
            form = InformeForm(instance=informe)
            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes

        return render(request, 'vista_profe/editar_informe.html', {'form': form, 
                                                                'informe': informe,
                                                                'grbas_form': grbas_form,
                                                                'rasati_form': rasati_form,
                                                                'tipo_usuario': tipo_usuario})

def eliminar_informe(request, informe_id):
    informe = get_object_or_404(Informe, id_informe=informe_id)
    tipo_informe = informe.tp_informe

    if tipo_informe == 'GRBAS':
        informe.grbas.delete()
    elif tipo_informe == 'RASATI':
        informe.rasati.delete()

    informe.delete()

    return redirect('listado_informes')


@user_passes_test(validate)
def detalle_informe(request, informe_id):

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        informe = get_object_or_404(Informe, id_informe=informe_id)

        try:
            grbas = Grbas.objects.get(id_informe=informe)
        except Grbas.DoesNotExist:
            grbas = None

        try:
            rasati = Rasati.objects.get(id_informe=informe)
        except Rasati.DoesNotExist:
            rasati = None

        # Obtén el paciente relacionado con este informe
        paciente_relacionado = informe.fk_relacion_pa_pro.id_paciente

    

    return render(request, 'vista_admin/detalle_informe.html', {
        'informe': informe,
        'grbas': grbas,
        'rasati': rasati,
        'paciente_relacionado': paciente_relacionado, 
        'tipo_usuario': tipo_usuario 
    })