from modelo_config_bd.config import *
from modelo_config_bd.modelo import *

@app.route('/')
def index():
    print('''Este é o Mundo Paranormal, 
    um projeto web que visa ajudar no gerenciamento das sessões de tabletopRPGs do sitema ordem paranormal''')
    print('''Github: https://github.com/andreluiz301/ficha-rpg-online''')
    #render_template('index.html')

@app.route('/cadastrar_mestre',methods=['POST'])
def cadastrar_mestre():
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        mestre = Mestre(userid=dados['user'],senha=dados['senha'])
        if (mestre.userid.repalce(old=' ',new='')) > 3:
            resposta = jsonify({'resultado':'user invalid'})
            return resposta
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
        jogador = Jogador(userid=dados['user'],senha=dados['senha'])
        if (jogador.userid.repalce(old=' ',new='')) > 3:
            resposta = jsonify({'resultado':'user invalid'})
            return resposta
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

@app.route('/login_mestre',methods=['POST'])
def logar_mestre():
    try:
        dados = request.json(force=True)
        user = db.session.query(Mestre).filter_by(userid=dados['user'],senha=dados['senha'])
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
                db.session.comit()
                resposta = jsonify({'resultado':'sucesso'})
            except Exception as e:
                resposta = jsonify({'resultado':'erro','detalhes':str(e)})
            return resposta
        elif identificador == 'complexo':
            try:
                dados = request.json(force=True)
                personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()
                if dados['nex'] is not None:
                    personagem.nex = dados['nex']
                if dados['vd_max'] is not None:
                    personagem.vd_max = dados['vd_max']
                    personagem.vd_atual = dados['vd_max']
                if dados['san_max'] is not None:
                    personagem.san_max = dados['san_max']
                    personagem.san_atual = dados['san_max']
                if dados['pe_max'] is not None:
                    personagem.pe_max = dados['pe_max']
                    personagem.pe_atual = dados['pe_max']
                if dados['forca'] is not None:
                    personagem.forca = dados['forca']
                if dados['agi'] is not None:
                    personagem.agi = dados['agi']
                if dados['int'] is not None:
                    personagem.int = dados['int']
                if dados['vig'] is not None:
                    personagem.vig = dados['vig']
                if dados['pre'] is not None:
                    personagem.pre = dados['pre']
                if dados['nome'] is not None:
                    personagem.nome = dados['nome']
                db.session.comit()
            except Exception as e:
                resposta = jsonify({'resultado':'erro','detalhes':str(e)})
            return resposta

@app.route('/deletar_personagem', methods = ['Delete'])
def deletar_personagem():
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force = True)
        personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()
        db.session.delete(personagem)
        db.session.commit
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta
    
