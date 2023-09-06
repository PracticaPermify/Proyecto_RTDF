# En tu_app/forms.py
from django import forms
from .models import Usuario, TpUsuario  # Importa tus modelos

class RegistroForm(forms.ModelForm):

    tipo_usuario = forms.ModelChoiceField(
        queryset=TpUsuario.objects.all(),
        empty_label=None,  # Elimina la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    class Meta:
        model = Usuario  # Modelo de usuario
        fields = ['numero_identificacion', 'primer_nombre', 'segundo_nombre', 'ap_paterno', 'ap_materno', 'fecha_nacimiento', 'email', 'numero_telefonico', 'password']  # Campos a mostrar en el formulario
