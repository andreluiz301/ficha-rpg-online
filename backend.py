from modelo_config_bd.config import *
from modelo_config_bd.modelo import *

@app.route('/')
def index():
    render_template('index.html')

@app.route('/cadastrar_mestre')
def cadastrar_mestre():
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        mestre = Mestre(userid=dados['user'],senha=dados['senha'])
        db.session.add(mestre)
        db.session.commit()
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resposta':'erro','detalhes':str(e)})
    return resposta

@app.route('/cadastrar_jogador')
def cadastrar_jogador():
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        mestre = Jogador(userid=dados['user'],senha=dados['senha'])
        db.session.add(mestre)
        db.session.commit()
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resposta':'erro','detalhes':str(e)})
    return resposta

@app.route('/login_jogador')
def logar_jogador():
    try:
        dados = request.json(force=True)
        user = db.session.query(Jogador).filter_by(userid=dados['user'],senha=dados['senha'])
        if user == None:
            resposta = jsonify({'resultado':'not user'})
        jw_token = create_access_token(identity=user.userid)
        resposta  = jsonify({'resultado':'sucesso','jwt':jw_token})
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

@app.route('/criar_personagem')
def criar_personagem():

