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
        queryset=TpInforme.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Tipo de Informe'
    )

    class Meta:
        model = Informe  # Especifica el modelo que se utilizará en el formulario
        fields = ['fk_relacion_pa_pro', 'titulo', 'descripcion', 'fecha', 'observacion', 'tp_informe']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }