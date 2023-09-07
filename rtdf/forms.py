from django import forms
from .models import Usuario, TpUsuario

# Define la variable TIPO_USUARIO aquí

class RegistroForm(forms.ModelForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset=TpUsuario.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    class Meta:
        model = Usuario
        fields = ['numero_identificacion', 'primer_nombre', 'segundo_nombre', 'ap_paterno', 'ap_materno', 'fecha_nacimiento', 'email', 'numero_telefonico', 'password', 'tipo_usuario']
