from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def inicio():
    datos = {
        'nombre': 'Luis González',
        'descripcion': 'Desarrollador web y entusiasta de la tecnología.',
        'redes': {
            'GitHub': 'https://github.com/usuario',
            'LinkedIn': 'https://linkedin.com/in/usuario',
            'Twitter': 'https://twitter.com/usuario'
        }
    }
    return render_template('index.html', **datos)
