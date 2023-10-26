from django import forms
from .models import *
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re
from django.core import validators

##Numero de telefono

def es_numero_telefonico_valido(numero_telefonico):

    patron = r'^\+\d{56}$'
    return re.match(patron, numero_telefonico) is not None

def es_password_valido(password):

    if not re.search(r'[A-Z]', password):
        raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')

    if not re.search(r'[a-z]', password):
        raise ValidationError('La contraseña debe contener al menos una letra minúscula.')

    if not re.search(r'[0-9]', password):
        raise ValidationError('La contraseña debe contener al menos un número.')

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('La contraseña debe contener al menos un carácter especial.')

    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    
def clean_rut_paciente(self):
        rut = self.cleaned_data['rut_paciente']
        # Realiza aquí las validaciones del RUT y devuelve el valor limpio o lanza ValidationError si es inválido
        if not re.match(r'^\d{7,8}-[Kk\d]$', rut):
            raise forms.ValidationError('El RUT ingresado no es válido.')
        return rut

##Caracteres obligatorios para la contraseña

class RegistroForm(forms.ModelForm):

    numero_identificacion = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'}),
        help_text='Ingrese su RUT válido (Ejemplo: 12345678-9)',
        label='Rut',
        validators=[
            validators.RegexValidator(
                regex=r'^\d{7,8}-[Kk\d]$',  # Validador para RUTs en formato válido
                message='Ingrese un RUT válido en formato 12345678-9.'
            ),
            validators.MinLengthValidator(limit_value=9, message='El rut debe contar con los caracteres especificados'),  
        ]
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        required=True
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'usuario@gmail.com'}),
        validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida")],
        required=True
    )

    numero_telefonico = forms.CharField(
        validators=[es_numero_telefonico_valido],
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+56912345678'}),
        help_text='Ingrese un número de teléfono válido (Ejemplo: +56912345678)'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        validators=[es_password_valido],
        required=True,
        help_text='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.'
    )

    tipo_usuario = forms.ModelChoiceField(
        queryset=TpUsuario.objects.filter(tipo_usuario__in=['Paciente', 'Familiar']),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'tipo_usuario'}),
        label='Tipo de usuario'
    )

    id_comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Comuna'
    )

    telegram = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Telegram'}),
        help_text='Ingrese su usuario de Telegram (opcional)'
    )

    fk_tipo_hipertension = forms.ModelChoiceField(
        queryset=TipoHipertension.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Tipo de Hipertensión'
    )

    fk_tipo_diabetes = forms.ModelChoiceField(
        queryset=TipoDiabetes.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Tipo de Diabetes'
    )

    fk_tipo_familiar = forms.ModelChoiceField(
        queryset=TpFamiliar.objects.all(),  # Ajusta esto según tus necesidades
        required=False,  # Cambia esto a True si el campo es obligatorio para Familiares
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Parentesco con paciente'
    )

    rut_paciente = forms.CharField(
        max_length=12,  # Ajusta la longitud máxima según tus necesidades
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'}),
        help_text='Ingresa el RUT del paciente (Ejemplo: 12345678-9)',
        label='Rut del paciente',
        validators=[
            validators.RegexValidator(
                regex=r'^\d{7,8}-[Kk\d]$',  # Validador para RUTs en formato válido
                message='Ingrese un RUT válido en formato 12345678-9.'
            ),
            validators.MinLengthValidator(limit_value=9, message='El rut debe contar con los caracteres especificados'),
        ],
    )

    class Meta:
        model = Usuario
        fields = ['numero_identificacion', 
                  'primer_nombre', 
                  'segundo_nombre', 
                  'ap_paterno', 
                  'ap_materno', 
                  'fecha_nacimiento', 
                  'email', 
                  'numero_telefonico', 
                  'id_comuna',
                  'password',
                  'tipo_usuario',
                  'telegram',  # Campo para Paciente
                  'fk_tipo_hipertension',  # Campo para Paciente
                  'fk_tipo_diabetes',  # Campo para Paciente
                  'fk_tipo_familiar', #Campo para familiar
                  'rut_paciente'
                  ]


class InformeForm(forms.ModelForm):
    fk_relacion_pa_pro = forms.ModelChoiceField(
        queryset=RelacionPaPro.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Relación con Paciente y Profesional de Salud'
    )

    titulo = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Vocalización/Intensidad'}),
        label='Título'
    )

    descripcion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Descripción'}),
        label='Descripción'
    )

    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d-%m-%Y', attrs={'placeholder': 'día-mes-año'}),
        required=True
    )

    observacion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Añadir detalles de los síntomas.'}),
        label='Observación'
    )

    tp_informe = forms.ModelChoiceField(
        queryset=TpInforme.objects.filter(tipo_informe__in=['RASATI', 'GRBAS']),
        required=False,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm','id': 'tp_informe'}),
        label='Tipo de Informe'
    )

    class Meta:
        model = Informe  
        fields = [
            'fk_relacion_pa_pro', 
            'titulo', 
            'descripcion', 
            'fecha', 
            'observacion', 
            'tp_informe'
        ]

        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

OPCIONES_GRBAS = [
        (0, 'Normal'),
        (1, 'Leve'),
        (2, 'Moderado'),
        (3, 'Alteración Severa'),
    ]

class GrbasForm(InformeForm):
    g_grado_disfonia = forms.ChoiceField(
        label='Grado de Disfonía',
        choices=OPCIONES_GRBAS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    r_aspereza = forms.ChoiceField(
        label='r_aspereza',
        choices=OPCIONES_GRBAS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    b_soplo = forms.ChoiceField(
        label='b_soplo',
        choices=OPCIONES_GRBAS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    a_debilidad = forms.ChoiceField(
        label='a_debilidad',
        choices=OPCIONES_GRBAS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    s_tension = forms.ChoiceField(
        label='s_tension',
        choices=OPCIONES_GRBAS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Grbas
        fields = InformeForm.Meta.fields + ['g_grado_disfonia', 'r_aspereza', 'b_soplo', 'a_debilidad', 's_tension']

OPCIONES_RASATI = [
        (0, 'Normal'),
        (1, 'Alteración leve'),
        (2, 'Alteración moderada'),
        (3, 'Alteración severa'),
    ]

class RasatiForm(InformeForm):
    r_ronquedad = forms.ChoiceField(
        label='r_ronquedad',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    a_aspereza = forms.ChoiceField(
        label='a_aspereza',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    s_soplo = forms.ChoiceField(
        label='s_soplo',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    a_astenia = forms.ChoiceField(
        label='a_astenia',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    t_tension = forms.ChoiceField(
        label='t_tension',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    i_inestabilidad = forms.ChoiceField(
        label='i_inestabilidad',
        choices=OPCIONES_RASATI,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Rasati
        fields = InformeForm.Meta.fields + ['r_ronquedad', 'a_aspereza', 's_soplo', 'a_astenia', 't_tension', 'i_inestabilidad']            


class PautaTerapeuticaForm(forms.ModelForm):

    cant_veces_dia = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Número de veces al día'}),
        label='Título'
    )

    descripcion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Descripción'}),
        label='Descripción'
    )

    fecha_inicio = forms.DateTimeField(
         widget=forms.DateTimeInput(format='%d-%m-%Y', attrs={'placeholder': 'día-mes-año'}),
         required=True
     )

    fecha_fin = forms.DateTimeField(
         widget=forms.DateTimeInput(format='%d-%m-%Y', attrs={'placeholder': 'día-mes-año'}),
         required=True
     )

    comentario = forms.CharField(
         required=True,
         widget=forms.Textarea(attrs={'placeholder': 'Añadir comentarios'}),
         label='Observación'
    )

    fk_tp_terapia = forms.ModelChoiceField(
        queryset=TpTerapia.objects.filter(tipo_terapia__in=['Vocalización', 'Intensidad']),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Tipo de terapia'
    )

    class Meta:
        model = PautaTerapeutica
        fields = ['cant_veces_dia', 'descripcion', 'fecha_inicio', 'fecha_fin', 'comentario', 'fk_tp_terapia']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class VocalizacionForm(PautaTerapeuticaForm):

    duracion_seg = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Duración en segundos'}),
        required=False,
        label='Duración en segundos'
    )

    bpm = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ingresar BPM necesario'}),
        required=False,
        label='BPM'
    )

    tempo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ingresar Tempo en segundos'}),
        required=False,
        label='Tempo'
    )

    class Meta:
        model = Vocalizacion
        fields = PautaTerapeuticaForm.Meta.fields + ['duracion_seg', 'bpm', 'tempo']

class IntensidadForm(PautaTerapeuticaForm):

    intensidad = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Intensidad'}),
        required=False,
        label='Duración en segundos'
    )

    min_db = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'dB mínimo'}),
        required=False,
        label='BPM'
    )

    max_db = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'dB máximo'}),
        required=False,
        label='BPM'
    )

    class Meta:
        model = Intensidad
        fields = PautaTerapeuticaForm.Meta.fields + ['intensidad', 'min_db','max_db']


class AudioscoeficientesForm(forms.ModelForm):

    nombre_archivo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del audio'}),
        required=False,
        label='Nombre audio'
    )    

    fk_tipo_llenado = forms.ModelChoiceField(queryset=TpLlenado.objects.all(),
        required=False,  # Cambia esto a True si el campo es obligatorio para Familiares
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
    )
    

    id_audio = forms.ModelChoiceField(queryset=Audio.objects.all(),
        required=False,  # Cambia esto a True si el campo es obligatorio para Familiares
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
    )
    

    fecha_coeficiente = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d-%m-%Y', attrs={'placeholder': 'día-mes-año'}),
        required=False
    )

    f0 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coeficiente f0'}),
        required=False,
        label='Coeficiente f0'
    ) 

    f1 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coeficiente f1'}),
        required=False,
        label='Coeficiente f1'
    )    

    f2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coeficiente f2'}),
        required=False,
        label='Coeficiente f2'
    )    

    f3 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coeficiente f3'}),
        required=False,
        label='Coeficiente f3'
    )    

    f4 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coeficiente f4'}),
        required=False,
        label='Coeficiente f4'
    )       

    intensidad = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Intensidad'}),
        required=False,
        label='Intensidad'
    )

    hnr = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'HNR'}),
        required=False,
        label='HNR'
    )

    local_jitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Local Jitter'}),
        required=False,
        label='Local Jitter'
    )

    local_absolute_jitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Local Absolute Jitter'}),
        required=False,
        label='Local Absolute Jitter'
    )

    rap_jitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'RAP Jitter'}),
        required=False,
        label='RAP Jitter'
    )

    ppq5_jitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'PPQ5 Jitter'}),
        required=False,
        label='PPQ5 Jitter'
    )

    ddp_jitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'DDP Jitter'}),
        required=False,
        label='DDP Jitter'
    )

    local_shimmer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Local Shimmer'}),
        required=False,
        label='Local Shimmer'
    )

    local_db_shimmer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Local dB Shimmer'}),
        required=False,
        label='Local dB Shimmer'
    )

    apq3_shimmer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'APQ3 Shimmer'}),
        required=False,
        label='APQ3 Shimmer'
    )

    aqpq5_shimmer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'APQ5 Shimmer'}),
        required=False,
        label='APQ5 Shimmer'
    )

    apq11_shimmer = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'APQ11 Shimmer'}),
        required=False,
        label='APQ11 Shimmer'
    )    



    class Meta:
        model = Audioscoeficientes  
        fields = ['nombre_archivo','fk_tipo_llenado','id_audio','fecha_coeficiente'
                  ,'f0','f1','f2','f3','f4','intensidad','hnr','local_jitter',
                  'local_absolute_jitter','rap_jitter','ppq5_jitter','ddp_jitter',
                  'local_shimmer','local_db_shimmer','apq3_shimmer','aqpq5_shimmer'
                  ,'apq11_shimmer']
        

        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


#Inicio de la pesadilla

class PreRegistroForm(forms.ModelForm):

    numero_identificacion = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'}),
        help_text='Ingrese su RUT válido (Ejemplo: 12345678-9)',
        label='Rut'
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        required=False
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'usuario@gmail.com'}),
        validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida")],
        required=True
    )

    numero_telefonico = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+56912345678'}),
        help_text='Ingrese un número de teléfono válido (Ejemplo: +56912345678)'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        required=False,
        help_text='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.'
    )

    tipo_usuario = forms.ModelChoiceField(
        queryset=TpUsuario.objects.filter(tipo_usuario__in=['Fonoaudiologo', 'Neurologo', 'Enfermera']),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'tipo_usuario'}),
        label='Tipo de usuario'
    )

    id_comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Comuna'
    )

    id_institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Institución'
    )

    class Meta:
        model = PreRegistro
        fields = ['numero_identificacion', 
                  'primer_nombre', 
                  'segundo_nombre', 
                  'ap_paterno', 
                  'ap_materno', 
                  'fecha_nacimiento', 
                  'email', 
                  'numero_telefonico', 
                  'id_comuna',
                  'password',
                  'tipo_usuario',
                  'id_institucion',
                  ]
        
    # def clean(self):
    #     cleaned_data = super().clean()

    #     fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
    #     if not fecha_nacimiento:
    #         raise forms.ValidationError("La fecha de nacimiento es requerida.")

    #     return cleaned_data
