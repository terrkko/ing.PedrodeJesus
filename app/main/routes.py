from flask import render_template
from . import main_bp  # Importamos el blueprint definido en __init__.py

@main_bp.route('/')
def inicio():
    datos = {
        'nombre': 'Pagina Personal',
        'descripcion': 'Desarrollador web y entusiasta de la tecnología.',
        'redes': {
            'GitHub': 'https://github.com/usuario',
            'LinkedIn': 'https://linkedin.com/in/usuario',
            'Twitter': 'https://twitter.com/usuario'
        }
    }
    return render_template('index.html', **datos)
