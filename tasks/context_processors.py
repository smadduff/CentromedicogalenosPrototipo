# context_processors.py en una de tus apps, por ejemplo, 'miapp'

from .models import Perfil

def add_tipo_usuario_to_context(request):
    if not request.user.is_authenticated:
        return {}
    try:
        perfil = request.user.perfil
        return {'tipo_usuario': perfil.tipo_usuario}
    except Perfil.DoesNotExist:
        # Si el usuario no tiene perfil, puedes decidir qué hacer
        return {'tipo_usuario': None}
