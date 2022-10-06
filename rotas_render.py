from modelo_config_bd.config import *
from modelo_config_bd.modelo import *

@app.route('/render_login')
def render_login():
    render_template('login.html')

@app.route('/render_cadastro')
def render_Cadastro():
    render_template('cadatro.html')