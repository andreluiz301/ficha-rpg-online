from modelo_config_bd.config import *
from modelo_config_bd.modelo import *

@app.route('/')
def index():
    render_template('index.html')

@app.route('/cadastrar_mestre',methods=['POST'])
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

@app.route('/cadastrar_jogador',methods=['POST'])
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

@app.route('/login_jogador',methods=['POST'])
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

@app.route('/criar_personagem',methods=['POST'])
def criar_personagem():
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.get_json(force=True)
        personagem = Personagem(**dados)
        db.session.add(personagem)
        db.session.commit()
        personagem2 = db.session.query(Personagem.id).filter_by(jogadorid=dados['jogadorid']).first()
        resposta = jsonify({'resultado':'sucesso','detalhes':'id'})
    except Exception as e :
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

@app.route('/listar/<string:identificador',methods = ['POST']) # Rota generica.
def listar(identificador):
    try:
        dados = request.get_json(force=True)
        if identificador == 'Player':
            person = db.session.query(Personagem).filter_by(id = dados['id']).first()
            personagem = person.retorna_personagem()
            resposta = personagem
        elif identificador == 'Mestre':
            personagem =  db.session.query(Personagem).filter_by(mestreid = dados['id']).all()
            person_json =[ x.retorna_personagem() for x in personagem ]
            resposta = personagem
        elif identificador == 'Inventario':
            inventario = db.session.query(Inventario).filter_by(personagem=dados['id']).all()
            itens_json =[ x.retorna_item() for x in inventario]
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

@app.route('/update_persongem/<string:identificador>',methods=['PUT'])
def update_personagem_simples(identificador):
        if identificador == 'simples':    
            try:
                dados = request.get_json(force=True)
                personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()
                if dados['dano_sofrido'] is not None:
                    personagem.vd_atual = personagem.vd_atual - dados['dano_sofrido']
                if dados['cura'] is not None:
                    personagem.vd_atual = personagem.vd_atual + dados['cura']
                if dados['dano_mental'] is not None:
                    personagem.san_atual = personagem.san_atual - dados['dano_mental']
                if dados['san_regen'] is not None:
                    personagem.san_atual = personagem.san_atual + dados['san_regen']
                resposta = jsonify({'resultado':'sucesso'})
            except Exception as e:
                resposta = jsonify({'resultado':'erro','detalhes':str(e)})
            return resposta
        if identificador == 'complexo':
