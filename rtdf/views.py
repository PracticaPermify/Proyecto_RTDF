from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_exempt
#from django.core.files.storage import default_storage
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
#import wave
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from rtdf.audio_coef import audio_analysis
#from rtdf.audio_coef import *
#import scripts as scripts

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
        
        if tipo_usuario == 'Paciente':
            paciente = Paciente.objects.get(id_usuario=request.user)

            now = timezone.now()
            pautas_terapeuticas = PautaTerapeutica.objects.filter(
                fk_informe__fk_relacion_pa_pro__id_paciente=paciente,
                fecha_fin__gte=now 
            )

            pautas_terapeuticas_expiradas = PautaTerapeutica.objects.filter(
                fk_informe__fk_relacion_pa_pro__id_paciente=paciente,
                fecha_fin__lt=now 
            )

            paginador = Paginator(pautas_terapeuticas_expiradas, 5)
            page_number = request.GET.get('page')
            pautas_terapeuticas_expiradas = paginador.get_page(page_number)

            return render(request, 'rtdf/index.html', {'tipo_usuario': tipo_usuario, 
                                                       'usuario': usuarios,
                                                       'pautas_terapeuticas': pautas_terapeuticas,
                                                       'pautas_terapeuticas_expiradas': pautas_terapeuticas_expiradas,})
    
    usuarios_por_pagina = 10  
    paginator = Paginator(usuarios, usuarios_por_pagina)  

    page_number = request.GET.get('page')

    # Obtiene la página actual de usuarios
    page = paginator.get_page(page_number)

    return render(request, 'rtdf/index.html', {'tipo_usuario': tipo_usuario, 
                                               'usuario': page})

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
                'segundo_nombre': relacion.id_paciente.id_usuario.segundo_nombre,
                'ap_paterno': relacion.id_paciente.id_usuario.ap_paterno,
                'ap_materno': relacion.id_paciente.id_usuario.ap_materno,
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

                # asociar el informe con VOCALIZACION O INTENSIDAD
                if tipo_terapia == 'Vocalización':
                    
                    vocalizacion = vocalizacion_form.save(commit=False)
                    vocalizacion.id_pauta_terapeutica = pauta_terapeutica
                    vocalizacion.save()

                elif tipo_terapia == 'Intensidad':
                        
                    #se obtiene en valor del campo validado del form y se compara que este vacio    
                    if not intensidad_form.cleaned_data['min_db']:
                        #se setea a null
                        intensidad_form.cleaned_data['min_db'] = None

                    if not intensidad_form.cleaned_data['max_db']:
                        intensidad_form.cleaned_data['max_db'] = None   

                    #antes de guardar el formulario se setea el campo de min db y max db
                    intensidad_form.instance.min_db = intensidad_form.cleaned_data['min_db']
                    intensidad_form.instance.max_db = intensidad_form.cleaned_data['max_db']

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
def vocalizacion(request, pauta_id=None, *args, **kwargs):
    tipo_usuario = None
    pauta_seleccionada = None
    

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # Obtén el nombre de usuario y su ID
        nombre_usuario = f"{request.user.primer_nombre}_{request.user.ap_paterno}"
        id_usuario = request.user.id_usuario
        fecha = timezone.now()
        fecha_formateada = fecha.strftime("%Y-%m-%d_%H-%M-%S")

        # Crea una ruta para la carpeta del usuario
        carpeta_usuario = os.path.join(settings.MEDIA_ROOT, 'audios_pacientes', nombre_usuario)

        # Verifica si la carpeta del usuario existe, si no, créala
        if not os.path.exists(carpeta_usuario):
            os.makedirs(carpeta_usuario)

        id_pauta = None
        tipo_pauta = None

        if pauta_id is not None:
            try:
                pauta_seleccionada = PautaTerapeutica.objects.get(id_pauta_terapeutica=pauta_id)
                id_pauta = pauta_seleccionada.id_pauta_terapeutica
                tipo_pauta = pauta_seleccionada.fk_tp_terapia.tipo_terapia 
                id_profesional = pauta_seleccionada.fk_informe.fk_relacion_pa_pro.fk_profesional_salud.id_profesional_salud
                request.session['id_pauta'] = id_pauta  
                request.session['tipo_pauta'] = tipo_pauta
                request.session['id_profesional'] = id_profesional
                #print("ID PROFESIONAL", id_profesional)
            except PautaTerapeutica.DoesNotExist:
                pauta_seleccionada = None
       

    if request.method == 'POST':
        audio_file = request.FILES.get('file')
        print("Estoy llegando aquí", audio_file)

        # se obtiene variables declaradas en la sesion
        id_pauta = request.session.get('id_pauta', None)
        tipo_pauta = request.session.get('tipo_pauta', None)
        id_profesional = request.session.get('id_profesional', None)

        # Define el nombre del archivo con el nombre del usuario y su ID
        nombre_archivo = f"{nombre_usuario}_{id_usuario}_{fecha_formateada}_{tipo_pauta}_{id_pauta}_{id_profesional}_audio.wav"
        ruta_archivo = os.path.join(carpeta_usuario, nombre_archivo)

        # se elimina la variable de la sesion y se guarda en la DB
        if id_pauta is not None:

            # contruccion de la url para la tabla audio DB
            if tipo_pauta == "Vocalización":
                origen_audio = OrigenAudio.objects.get(id_origen_audio=2)
                
            else:
                origen_audio = OrigenAudio.objects.get(id_origen_audio=1)

            fk_pauta = PautaTerapeutica.objects.get(id_pauta_terapeutica=id_pauta)

            ruta_db = f"{nombre_usuario}/{nombre_archivo}"
            ##print("Ruta para la db:", ruta_db)

            audio_model = Audio.objects.create(url_audio=ruta_db,
                                               fecha_audio=fecha,
                                               fk_origen_audio=origen_audio,
                                               fk_pauta_terapeutica=fk_pauta)
            audio_model.save()

            id_audio_registrado = audio_model.id_audio


            # Guarda el archivo en la carpeta del usuario con el nuevo nombre
            if audio_file:
                with open(ruta_archivo, 'wb') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)


            #REGISTRO DE LOS COEFICIENTES DE AUDIOS DE VOCALIZACION EN LA DB

            #obtencion del tipo de llenado automatico
            tipo_llenado = TpLlenado.objects.get(id_tipo_llenado=1)

            #obtencion del id del audio
            id_audio = Audio.objects.get(id_audio=id_audio_registrado)

            print(ruta_db)
            res = audio_analysis(ruta_db, nombre_archivo, fecha)
            is_coefs=Audioscoeficientes.objects.all().filter(nombre_archivo=nombre_archivo)
            # id_user=int(username.split(' ')[0])
            if not is_coefs.exists():
                print('analizando')
                coefs=Audioscoeficientes.objects.create(
                    nombre_archivo = nombre_archivo,
                    fecha_coeficiente = res['date'],               
                    f0  = res['f0'],
                    f1  = res['f1'],
                    f2  = res['f2'],
                    f3  = res['f3'],
                    f4  = res['f4'],
                    intensidad  = res['Intensity'],
                    hnr  = res['HNR'],
                    local_jitter  = res['localJitter'],
                    local_absolute_jitter  = res['localabsoluteJitter'],
                    rap_jitter  = res['rapJitter'],
                    ppq5_jitter  = res['ppq5Jitter'],
                    ddp_jitter = res['ddpJitter'],
                    local_shimmer = res['localShimmer'],
                    local_db_shimmer = res['localdbShimmer'],
                    apq3_shimmer = res['apq3Shimmer'],
                    aqpq5_shimmer = res['aqpq5Shimmer'],
                    apq11_shimmer = res['apq11Shimmer'],
                    fk_tipo_llenado = tipo_llenado, 
                    id_audio = id_audio
                )
                coefs.save()
                print('analizado')


            # del request.session['id_pauta']
            # del request.session['tipo_pauta']



    return render(request, 'vista_paciente/vocalizacion.html', {'tipo_usuario': tipo_usuario,
                                                               'pauta_seleccionada': pauta_seleccionada})



@user_passes_test(validate)
def intensidad(request, pauta_id=None, *args, **kwargs):

    tipo_usuario = None
    pautas_terapeuticas = None
    pauta_seleccionada = None

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # Obtén el nombre de usuario y su ID
        nombre_usuario = f"{request.user.primer_nombre}_{request.user.ap_paterno}"
        id_usuario = request.user.id_usuario
        fecha = timezone.now()
        fecha_formateada = fecha.strftime("%Y-%m-%d-%H-%M-%S")

        # Crea una ruta para la carpeta del usuario
        carpeta_usuario = os.path.join(settings.MEDIA_ROOT, 'audios_pacientes', nombre_usuario)

        # Verifica si la carpeta del usuario existe, si no, créala
        if not os.path.exists(carpeta_usuario):
            os.makedirs(carpeta_usuario)

        id_pauta = None
        tipo_pauta = None

        if pauta_id is not None:
            try:
                pauta_seleccionada = PautaTerapeutica.objects.get(id_pauta_terapeutica=pauta_id)
                id_pauta = pauta_seleccionada.id_pauta_terapeutica
                tipo_pauta = pauta_seleccionada.fk_tp_terapia.tipo_terapia 
                id_profesional = pauta_seleccionada.fk_informe.fk_relacion_pa_pro.fk_profesional_salud.id_profesional_salud
                request.session['id_pauta'] = id_pauta  
                request.session['tipo_pauta'] = tipo_pauta
                request.session['id_profesional'] = id_profesional
            except PautaTerapeutica.DoesNotExist:
                pauta_seleccionada = None

    if request.method == 'POST':
        audio_file = request.FILES.get('file')
        print("Estoy llegando aquí", audio_file)

        # se obtiene variables declaradas en la sesion
        id_pauta = request.session.get('id_pauta', None)
        tipo_pauta = request.session.get('tipo_pauta', None)
        id_profesional = request.session.get('id_profesional', None)

        # Define el nombre del archivo con el nombre del usuario y su ID
        nombre_archivo = f"{nombre_usuario}_{id_usuario}_{fecha_formateada}_{tipo_pauta}_{id_pauta}_{id_profesional}_audio.wav"
        ruta_archivo = os.path.join(carpeta_usuario, nombre_archivo)

        # se elimina la variable de la sesion y se guarda en la DB
        if id_pauta is not None:

            # contruccion de la url para la DB
            if tipo_pauta == "Intensidad":
                origen_audio = OrigenAudio.objects.get(id_origen_audio=1)
            else:
                origen_audio = OrigenAudio.objects.get(id_origen_audio=2)

            fk_pauta = PautaTerapeutica.objects.get(id_pauta_terapeutica=id_pauta)

            ruta_db = f"{nombre_usuario}/{nombre_archivo}"
            ##print("Ruta para la db:", ruta_db)

            audio_model = Audio.objects.create(url_audio=ruta_db,
                                               fecha_audio=fecha,
                                               fk_origen_audio=origen_audio,
                                               fk_pauta_terapeutica=fk_pauta)
            audio_model.save()

            #Capturo el id del audio al momento del guardado en la base de datos
            id_audio_registrado = audio_model.id_audio

            # Guarda el archivo en la carpeta del usuario con el nuevo nombre
            if audio_file:
                with open(ruta_archivo, 'wb') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)

            #REGISTRO DE LOS COEFICIENTES DE AUDIOS DE INTENSIDAD EN LA DB

            #obtencion del tipo de llenado automatico
            tipo_llenado = TpLlenado.objects.get(id_tipo_llenado=1)

            #obtencion del id del audio
            # id_audio = Audio.objects.get(id_audio=id_audio_registrado)

            print(ruta_db)
            res = audio_analysis(ruta_db, nombre_archivo, fecha)
            is_coefs=Audioscoeficientes.objects.all().filter(nombre_archivo=nombre_archivo)
            # id_user=int(username.split(' ')[0])
            if not is_coefs.exists():
                print('analizando')
                coefs=Audioscoeficientes.objects.create(
                    nombre_archivo = nombre_archivo,
                    fecha_coeficiente = fecha,                    
                    f0  = res['f0'],
                    f1  = res['f1'],
                    f2  = res['f2'],
                    f3  = res['f3'],
                    f4  = res['f4'],
                    intensidad  = res['Intensity'],
                    hnr  = res['HNR'],
                    local_jitter  = res['localJitter'],
                    local_absolute_jitter  = res['localabsoluteJitter'],
                    rap_jitter  = res['rapJitter'],
                    ppq5_jitter  = res['ppq5Jitter'],
                    ddp_jitter = res['ddpJitter'],
                    local_shimmer = res['localShimmer'],
                    local_db_shimmer = res['localdbShimmer'],
                    apq3_shimmer = res['apq3Shimmer'],
                    aqpq5_shimmer = res['aqpq5Shimmer'],
                    apq11_shimmer = res['apq11Shimmer'],
                    fk_tipo_llenado = tipo_llenado, 
                    id_audio = id_audio
                )
                coefs.save()
                print('analizado')


            # del request.session['id_pauta']
            # del request.session['tipo_pauta']

    return render(request,'vista_paciente/intensidad.html', {'tipo_usuario': tipo_usuario,
                                                            'pauta_seleccionada': pauta_seleccionada})
    
    
def esv(request):
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        profesional_salud = request.user.profesionalsalud
        relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        preguntas = [
            "¿Tiene dificultades para llamar la atención de los demás usando su voz?",
            "¿Tiene problemas al cantar?",
            "¿Le duele la garganta?",
            "¿Su voz está ronca?",
            "En conversaciones grupales, ¿Las personas tienen dificultades para escucharlo(a)?",
            "¿Suele perder su voz?",
            "¿Suele toser o carraspear?",
            "¿Considera que tiene una voz débil?",
            "¿Tiene problemas al hablar por teléfono?",
            "¿Se siente menos valorado o deprimido debido a su problema de la voz?",
            "¿Siente como si tuviera algo atascado en su garganta?",
            "¿Siente inflamación en la garganta?",
            "¿Siente pudor al usar su voz?",
            "¿Siente que se cansa al hablar?",
            "¿Su problema de la voz lo hace sentir estresado y nervioso?",
            "¿Tiene dificultades para hacerse escuchar cuando hay ruido en el ambiente?",
            "¿Es incapaz de gritar o alzar la voz?",
            "¿Su problema de la voz le genera complicaciones con su familia y amigos?",
            "¿Tiene mucha flema o mucosidad en su garganta?",
            "¿Siente que la calidad de su voz varía durante el día?",
            "¿Siente que a las personas les molesta su voz?",
            "¿Tiene la nariz tapada?",
            "¿La gente le pregunta qué le pasa a su voz?",
            "¿Siente que su voz suena ronca y seca?",
            "¿Siente que debe esforzarse para sacar la voz?",
            "¿Con cuánta frecuencia presenta infecciones en la garganta?",
            "¿Su voz se “agota” mientras está hablando?",
            "¿Su voz lo(a) hace sentir incompetente?",
            "¿Se siente avergonzado debido a su problema de la voz?",
            "¿Se siente aislado por sus problemas con la voz?"
        ]

        opciones_respuesta = ["Nunca", "Casi nunca", "A veces", "Casi siempre", "Siempre"]

        if request.method == 'POST':
            form = InformeForm(request.POST)
            if form.is_valid():
                form.instance.tp_informe = TpInforme.objects.get(tipo_informe='ESV')
                informe = form.save()
                informe.fecha = timezone.now()

                # Inicializa los puntajes para las subescalas
                puntaje_limitacion = 0
                puntaje_emocional = 0
                puntaje_fisico = 0

                for i, pregunta in enumerate(preguntas):
                    respuesta = request.POST.get(f"respuesta_{i + 1}")

                    if respuesta == "Nunca":
                        puntaje = 0
                    elif respuesta == "Casi nunca":
                        puntaje = 1
                    elif respuesta == "A veces":
                        puntaje = 2
                    elif respuesta == "Casi siempre":
                        puntaje = 3
                    else:
                        puntaje = 4

                    if i + 1 in [1, 2, 4, 5, 6, 8, 9, 14, 16, 17, 20, 23, 24, 25, 27]:
                        puntaje_limitacion += puntaje
                    elif i + 1 in [10, 13, 15, 18, 21, 28, 29, 30]:
                        puntaje_emocional += puntaje
                    elif i + 1 in [3, 7, 11, 12, 19, 22, 26]:
                        puntaje_fisico += puntaje

                puntaje_limitacion = min(puntaje_limitacion, 60)
                puntaje_emocional = min(puntaje_emocional, 32)
                puntaje_fisico = min(puntaje_fisico, 28)

                puntaje_total = puntaje_limitacion + puntaje_emocional + puntaje_fisico
                if puntaje_total > 120:
                    puntaje_total = 120

                # Crea instancias de Informe y ESV y guarda los datos
                esv_instance = Esv(id_informe=informe, total_esv=puntaje_total, limitacion=puntaje_limitacion,
                                    emocional=puntaje_emocional, fisico=puntaje_fisico)
                esv_instance.save()

                return redirect('listado_informes')
        else:
            form = InformeForm(initial={'fecha': timezone.now()})
            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes

    return render(request, 'vista_profe/esv.html', {
        'form': form,
        'tipo_usuario': tipo_usuario,
        'preguntas': preguntas,
        'opciones_respuesta': opciones_respuesta,
    })



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
    obtener_esv = Esv.objects.filter(id_informe__fk_relacion_pa_pro__id_paciente=traer_paciente)

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    informes_rasati = obtener_rasati 
    informes_grbas = obtener_grbas    
    informes_esv= obtener_esv

    return render(request, 'vista_admin/detalle_paciente.html', {
        'paciente': paciente,
        'tipo_usuario': tipo_usuario,
        'paciente_info': traer_paciente,
        'fonoaudiologos_asociados': fonoaudiologos_asociados,
        'informes_esv': informes_esv,
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

def eliminar_informe_admin(request, informe_id):
    informe = get_object_or_404(Informe, id_informe=informe_id)
    tipo_informe = informe.tp_informe

    if tipo_informe == 'GRBAS':
        informe.grbas.delete()
    elif tipo_informe == 'RASATI':
        informe.rasati.delete()

    informe.delete()

    return redirect('detalle_paciente')


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

        datos_vocalizacion = Vocalizacion.objects.filter(id_pauta_terapeutica__fk_informe=informe_id,id_pauta_terapeutica__fk_tp_terapia= 1)    
        datos_intensidad = Intensidad.objects.filter(id_pauta_terapeutica__fk_informe=informe_id,id_pauta_terapeutica__fk_tp_terapia= 2)

        # Obtén el paciente relacionado con este informe
        paciente_relacionado = informe.fk_relacion_pa_pro.id_paciente

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

                # asociar el informe con VOCALIZACION O INTENSIDAD
                if tipo_terapia == 'Vocalización':
                    
                    vocalizacion = vocalizacion_form.save(commit=False)
                    vocalizacion.id_pauta_terapeutica = pauta_terapeutica
                    vocalizacion.save()

                elif tipo_terapia == 'Intensidad':
                        
                    #se obtiene en valor del campo validado del form y se compara que este vacio    
                    if not intensidad_form.cleaned_data['min_db']:
                        #se setea a null
                        intensidad_form.cleaned_data['min_db'] = None

                    if not intensidad_form.cleaned_data['max_db']:
                        intensidad_form.cleaned_data['max_db'] = None   

                    #antes de guardar el formulario se setea el campo de min db y max db
                    intensidad_form.instance.min_db = intensidad_form.cleaned_data['min_db']
                    intensidad_form.instance.max_db = intensidad_form.cleaned_data['max_db']

                    intensidad = intensidad_form.save(commit=False)
                    intensidad.id_pauta_terapeutica = pauta_terapeutica
                    intensidad.save()    

                return redirect('detalle_informe', informe_id=informe.id_informe)
        

        else:
            # Si la solicitud no es POST, muestra el formulario en blanco
            form = PautaTerapeuticaForm()
            vocalizacion_form = VocalizacionForm()
            intensidad_form = IntensidadForm()

    return render(request, 'vista_admin/detalle_informe.html', {
        'form': form,
        'vocalizacion_form': vocalizacion_form,
        'intensidad_form': intensidad_form,
        'datos_vocalizacion': datos_vocalizacion,
        'datos_intensidad': datos_intensidad,
        'informe': informe,
        'grbas': grbas,
        'rasati': rasati,
        'paciente_relacionado': paciente_relacionado, 
        'tipo_usuario': tipo_usuario 
    })


def editar_informe_admin(request, informe_id):
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        
        informe = get_object_or_404(Informe, id_informe=informe_id)

        pk_profesional = informe.fk_relacion_pa_pro.fk_profesional_salud
        relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=pk_profesional)

        # for relacion in relaciones_pacientes:
        #   print(relacion)

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

            if form.is_valid():
                informe.fecha = timezone.now()
                form.save()

            if rasati_form and rasati_form.is_valid():
                rasati_form.save()

            if grbas_form and grbas_form.is_valid():
                grbas_form.save()

            return redirect('detalle_informe', informe_id=informe.id_informe)
        else:
            form = InformeForm(instance=informe)
            form.fields['fk_relacion_pa_pro'].queryset = relaciones_pacientes

        return render(request, 'vista_admin/editar_informe_admin.html', {'form': form, 
                                                                        'informe': informe,
                                                                        'grbas_form': grbas_form,
                                                                        'rasati_form': rasati_form,
                                                                        'tipo_usuario': tipo_usuario})
    
def pacientes_disponibles(request):
    tipo_usuario = None 

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        pacientes_disponibles = Paciente.objects.filter(relacionpapro__isnull=True)

        return render(request, 'vista_profe/pacientes_disponibles.html', {'tipo_usuario': tipo_usuario, 
                                                                          'pacientes_disponibles': pacientes_disponibles})
    
def agregar_paciente(request, paciente_id):
    if request.user.is_authenticated and request.user.id_tp_usuario.tipo_usuario == 'Fonoaudiologo':
        profesional_salud = request.user.profesionalsalud
        paciente = Paciente.objects.get(pk=paciente_id)
        
        if RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud).count() < 10:

            if not RelacionPaPro.objects.filter(id_paciente=paciente).exists():
  
                relacion = RelacionPaPro(fk_profesional_salud=profesional_salud, id_paciente=paciente)
                relacion.save()
                return redirect('listado_pacientes')
            else:
                return render(request, 'vista_profe/error.html', {'error_message': 'El paciente ya está asignado a otro profesional.'})
        else:
            return render(request, 'vista_profe/error.html', {'error_message': 'Has alcanzado el límite de 10 pacientes asignados.'})
    else:
        return render(request, 'vista_profe/error.html', {'error_message': 'No tienes permiso para realizar esta acción.'})
    
def desvincular_paciente(request, paciente_id):

    paciente = get_object_or_404(Paciente, id_paciente=paciente_id)
    profesional_salud = request.user.profesionalsalud

    relacion = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud, id_paciente=paciente)
    
    if relacion.exists():
        relacion.delete()
        return redirect('listado_pacientes')
    else:
        return redirect('listado_pacientes')
    

def detalle_prof_pauta(request, id_pauta_terapeutica_id):

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        #print(tipo_usuario)

        pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)

        if tipo_usuario == 'Admin':
            url_regreso = reverse('detalle_prof_infor', kwargs={'informe_id': pauta.fk_informe.id_informe})
        elif tipo_usuario == 'Fonoaudiologo':
            url_regreso = reverse('detalle_prof_infor', kwargs={'informe_id': pauta.fk_informe.id_informe})
        else:
            url_regreso = reverse('detalle_prof_infor', kwargs={'informe_id': pauta.fk_informe.id_informe})

        

        try:
            intensidad = Intensidad.objects.get(id_pauta_terapeutica=pauta)
        except Intensidad.DoesNotExist:
            intensidad = None

        try:
            vocalizacion = Vocalizacion.objects.get(id_pauta_terapeutica=pauta)
        except Vocalizacion.DoesNotExist:
            vocalizacion = None

    # Obtén el paciente relacionado con este informe
    paciente_relacionado = pauta.fk_informe.fk_relacion_pa_pro.id_paciente

    return render(request, 'vista_profe/detalle_prof_pauta.html', {
        'tipo_usuario': tipo_usuario,
        'pauta' : pauta, 
        'intensidad' : intensidad,
        'vocalizacion': vocalizacion,
        'paciente_relacionado': paciente_relacionado,
        'url_regreso': url_regreso,

    })


def editar_prof_pauta(request, id_pauta_terapeutica_id):
 
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)
        profesional_salud = request.user.profesionalsalud
        relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        intensidad_form = None
        vocalizacion_form = None

        try:
            if pauta.intensidad:
                intensidad_form = IntensidadForm(request.POST or None, instance=pauta.intensidad)
        except Intensidad.DoesNotExist:
            intensidad_form = IntensidadForm()

        try:
            if pauta.vocalizacion:
                vocalizacion_form = VocalizacionForm(request.POST or None, instance=pauta.vocalizacion)
        except Vocalizacion.DoesNotExist:
            vocalizacion_form = VocalizacionForm()

        if request.method == 'POST':
            form = PautaTerapeuticaForm(request.POST, instance=pauta)

            if form.is_valid():
                form.save()

            if intensidad_form and intensidad_form.is_valid():
                intensidad_form.save()

            if vocalizacion_form and vocalizacion_form.is_valid():
                vocalizacion_form.save()

            return redirect('detalle_prof_pauta', id_pauta_terapeutica_id=pauta.id_pauta_terapeutica)
        else:
            form = PautaTerapeuticaForm(instance=pauta)


    return render(request, 'vista_profe/editar_prof_pauta.html', {
        'tipo_usuario': tipo_usuario,
        'pauta': pauta,
        'form': form, 
        'intensidad_form': intensidad_form,
        'vocalizacion_form': vocalizacion_form,


    })
    
def eliminar_prof_pauta(request, id_pauta_terapeutica_id):

    pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)
    tipo_pauta = pauta.fk_tp_terapia

    if tipo_pauta == 'Intensidad':
        pauta.intensidad.delete()
    elif tipo_pauta == 'Vocalización':
        pauta.vocalizacion.delete()

    pauta.delete()

    return redirect('detalle_prof_infor', informe_id=pauta.fk_informe.id_informe)


def detalle_pauta_admin(request, id_pauta_terapeutica_id):

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        #print(tipo_usuario)

        pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)

        if tipo_usuario == 'Admin':
            url_regreso = reverse('detalle_informe', kwargs={'informe_id': pauta.fk_informe.id_informe})
        elif tipo_usuario == 'Fonoaudiologo':
            url_regreso = reverse('detalle_prof_infor', kwargs={'informe_id': pauta.fk_informe.id_informe})
        else:
            url_regreso = reverse('detalle_prof_infor', kwargs={'informe_id': pauta.fk_informe.id_informe})

        

        try:
            intensidad = Intensidad.objects.get(id_pauta_terapeutica=pauta)
        except Intensidad.DoesNotExist:
            intensidad = None

        try:
            vocalizacion = Vocalizacion.objects.get(id_pauta_terapeutica=pauta)
        except Vocalizacion.DoesNotExist:
            vocalizacion = None

    # Obtén el paciente relacionado con este informe
    paciente_relacionado = pauta.fk_informe.fk_relacion_pa_pro.id_paciente

    return render(request, 'vista_admin/detalle_pauta_admin.html', {
        'tipo_usuario': tipo_usuario,
        'pauta' : pauta, 
        'intensidad' : intensidad,
        'vocalizacion': vocalizacion,
        'paciente_relacionado': paciente_relacionado,
        'url_regreso': url_regreso,
        })

def editar_pauta_admin(request, id_pauta_terapeutica_id):

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)
        # profesional_salud = request.user.profesionalsalud
        # relaciones_pacientes = RelacionPaPro.objects.filter(fk_profesional_salud=profesional_salud)

        intensidad_form = None
        vocalizacion_form = None

        try:
            if pauta.intensidad:
                intensidad_form = IntensidadForm(request.POST or None, instance=pauta.intensidad)
        except Intensidad.DoesNotExist:
            intensidad_form = IntensidadForm()

        try:
            if pauta.vocalizacion:
                vocalizacion_form = VocalizacionForm(request.POST or None, instance=pauta.vocalizacion)
        except Vocalizacion.DoesNotExist:
            vocalizacion_form = VocalizacionForm()

        if request.method == 'POST':
            form = PautaTerapeuticaForm(request.POST, instance=pauta)

            if form.is_valid():
                form.save()

            if intensidad_form and intensidad_form.is_valid():
                intensidad_form.save()

            if vocalizacion_form and vocalizacion_form.is_valid():
                vocalizacion_form.save()

            return redirect('detalle_pauta_admin', id_pauta_terapeutica_id=pauta.id_pauta_terapeutica)
        else:
            form = PautaTerapeuticaForm(instance=pauta)

    return render(request, 'vista_admin/editar_pauta_admin.html',{
        'tipo_usuario': tipo_usuario,
        'pauta': pauta,
        'form': form, 
        'intensidad_form': intensidad_form,
        'vocalizacion_form': vocalizacion_form,
    })

def eliminar_pauta_admin(request, id_pauta_terapeutica_id):

    pauta = get_object_or_404(PautaTerapeutica, id_pauta_terapeutica=id_pauta_terapeutica_id)
    tipo_pauta = pauta.fk_tp_terapia

    if tipo_pauta == 'Intensidad':
        pauta.intensidad.delete()
    elif tipo_pauta == 'Vocalización':
        pauta.vocalizacion.delete()

    pauta.delete()

    return redirect('detalle_informe', informe_id=pauta.fk_informe.id_informe)


def detalle_esv(request, informe_id):
    tipo_usuario = None 

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
        informe = get_object_or_404(Informe, pk=informe_id)
        paciente_relacionado = informe.fk_relacion_pa_pro.id_paciente

    return render(request, 'vista_profe/detalle_esv.html', {'informe': informe,
                                                            'tipo_usuario': tipo_usuario,
                                                            'paciente_relacionado': paciente_relacionado })


def editar_esv(request, informe_id):
    tipo_usuario = None
    
    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

    informe = get_object_or_404(Informe, pk=informe_id)

    if request.method == 'POST':
        informe.titulo = request.POST.get('titulo')
        informe.fecha = request.POST.get('fecha')
        informe.descripcion = request.POST.get('descripcion')
        informe.observacion = request.POST.get('observacion')
        informe.save()

        return redirect('listado_informes')
    else:
        return render(request, 'vista_profe/editar_esv.html', {'informe': informe, 
                                                                 'tipo_usuario': tipo_usuario})


def eliminar_informe_esv(request, informe_id):
    informe = get_object_or_404(Informe, id_informe=informe_id)
    esv_instance = Esv.objects.filter(id_informe=informe)

    if esv_instance.exists():
        esv_instance.delete()

    informe.delete()

    return redirect('listado_informes')


def detalle_esv_admin(request, informe_id):
    tipo_usuario = None 

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario
        informe = get_object_or_404(Informe, pk=informe_id)
        paciente_relacionado = informe.fk_relacion_pa_pro.id_paciente

    return render(request, 'vista_admin/detalle_esv_admin.html', {'informe': informe,
                                                            'tipo_usuario': tipo_usuario,
                                                            'paciente_relacionado': paciente_relacionado })

def eliminar_esv_admin(request, informe_id):
    informe = get_object_or_404(Informe, id_informe=informe_id)
    esv_instance = Esv.objects.filter(id_informe=informe)

    if esv_instance.exists():
        esv_instance.delete()

    informe.delete()

    return redirect('detalle_paciente', paciente_id=esv.paciente.id)

def analisis_admin(request):
    tipo_usuario = None

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # Actualiza esta consulta para incluir datos de Usuario
        datos_audiocoeficientes = Audioscoeficientes.objects.select_related(
            'id_audio__fk_pauta_terapeutica__fk_informe__fk_relacion_pa_pro__id_paciente__id_usuario',
            'id_audio__fk_pauta_terapeutica__fk_informe__fk_relacion_pa_pro__fk_profesional_salud'
        )

    return render(request, 'vista_admin/analisis_admin.html', {
        'tipo_usuario': tipo_usuario,
        'datos_audiocoeficientes': datos_audiocoeficientes
    })

def analisis_profe(request):
    tipo_usuario = None

    if request.user.is_authenticated:
        tipo_usuario = request.user.id_tp_usuario.tipo_usuario

        # Filtra datos de Audiocoeficientes para pacientes relacionados al profesional
        datos_audiocoeficientes = Audioscoeficientes.objects.select_related(
            'id_audio__fk_pauta_terapeutica__fk_informe__fk_relacion_pa_pro__id_paciente__id_usuario'
        ).filter(
            id_audio__fk_pauta_terapeutica__fk_informe__fk_relacion_pa_pro__fk_profesional_salud__id_usuario=request.user.id_usuario
        )

    return render(request, 'vista_profe/analisis_profe.html', {
        'tipo_usuario': tipo_usuario,
        'datos_audiocoeficientes': datos_audiocoeficientes
    })