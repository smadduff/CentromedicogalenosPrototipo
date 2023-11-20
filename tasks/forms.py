
from .models import Perfil
from django import forms
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, fields, Form



class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario', 'rut', 'direccion', 'imagen']
        labels = {
            'tipo_usuario': 'Tipo de usuario',
            'rut': 'RUT',
            'direccion': 'Dirección',
            'imagen': 'Imagen',
        }
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ActualizacionClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PerfilFormParaMisDatos(PerfilForm):
    class Meta(PerfilForm.Meta):  # Hereda de Meta en PerfilForm
        fields = ['rut', 'direccion', 'imagen']  # se removió 'tipo_usuario'


class RegistroAdminForm(UserCreationForm):
    rut = forms.CharField(
        max_length=15,
        required=True,
        label='RUT',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    direccion = forms.CharField(
        max_length=400,
        required=True,
        label='Dirección',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
    imagen = forms.ImageField(
        required=True,
        label='Imagen',
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )
    tipo_usuario = forms.ChoiceField(
        choices=Perfil.USUARIO_CHOICES,
        required=True,
        label='Tipo de usuario',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    password_generated = forms.CharField(
        label='Contraseña generada',
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=True,  # No se requiere ingresar valor en este campo
    )

    def generate_random_password(self):
        return get_random_string(length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'] = forms.CharField(widget=forms.HiddenInput(), required=False)
        self.fields['password2'] = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password_generated')  # Obtener la contraseña generada
        user.set_password(password)

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rut',
            'direccion',
            'imagen',
            'tipo_usuario',
            'password_generated',  # Agregar campo para mostrar la contraseña generada
        ]
