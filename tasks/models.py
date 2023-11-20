from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Paciente', 'Paciente'),
        ('Administrador', 'Administrador'),
        ('Medico', 'Medico'),
        ('Secretaria', 'Secretaria'),
        ('Cajero', 'Cajero')
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=20, blank=False, null=False, verbose_name='RUT')
    direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Dirección')
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')
    def acciones():
            return {
                'accion_eliminar': 'eliminar el Perfil',
                'accion_actualizar': 'actualizar el Perfil'
            }
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
    
#prueba - QVtWeaBd1m | secretaria - Q32914gWy5 | medico - WhMvz4U94A | cajero - TuaPt1uqe6 | paciente - awxvkTfrnc