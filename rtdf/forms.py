from django import forms
from .models import *
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re

##Campo de rut (errores para registrar con los caracteres correspondientes (CORREGIR))

def es_rut_valido(rut):
    rut = rut.replace(' ', '').replace('-', '')

    if not rut.isdigit() or not 8 <= len(rut) <= 10:
        return False

    numero_identificacion, digito_verificador = rut[:-1], rut[-1]

    try:
        numero_identificacion = int(numero_identificacion)
    except ValueError:
        return False

    suma = 0
    multiplo = 2
    for digito in reversed(str(numero_identificacion)):
        suma += int(digito) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    resto = suma % 11
    digito_esperado = 11 - resto if resto != 1 else 'K'

    return str(digito_esperado) == digito_verificador.upper()

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

##Caracteres obligatorios para la contraseña

class RegistroForm(forms.ModelForm):

    numero_identificacion = forms.CharField(
        validators=[es_rut_valido],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'}),
        help_text='Ingrese su RUT válido (Ejemplo: 12345678-9)',
        label='Rut'
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'día-mes-año'}),
        input_formats=['%d-%m-%Y', '%Y-%m-%d'],
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
        widget=forms.TextInput(attrs={'placeholder': '+56930304040'}),
        help_text='Ingrese un número de teléfono válido (Ejemplo: +56930304040)'
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
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Tipo de usuario'
    )

    id_comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label='Comuna'
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
                  'tipo_usuario',]


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['telegram', 'fk_tipo_hipertension', 'fk_tipo_diabetes']