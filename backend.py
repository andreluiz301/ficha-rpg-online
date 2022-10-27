from modelo_config_bd.config import *
from modelo_config_bd.modelo import *

@app.route('/')
def index():
    print('''Este é o Mundo Paranormal, 
    um projeto web que visa ajudar no gerenciamento das sessões de tabletopRPGs do sitema ordem paranormal''')
    print('''Github: https://github.com/andreluiz301/ficha-rpg-online''')
    #render_template('index.html')

@app.route('/cadastrar_mestre',methods=['POST']) # curl -X POST localhost:5000/cadastrar_mestre -d {'userid':'Spadez','senha':'123456789'} -H 'Content-Type: application/json'
def cadastrar_mestre():
    """Rota responsável por cadastrar um mestre.
    Returns:
        respostra(json): mensagem de sucesso caso tudo ocorre certo.
    """
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        mestre = Mestre(userid=dados['user'],senha=dados['senha'])
        if (mestre.userid.replace(old=' ',new='')) > 3: # Verifica se o usuário possui caracteres válidos.
            resposta = jsonify({'resultado':'user invalid'})
            return resposta
        db.session.add(mestre)
        db.session.commit()
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resposta':'erro','detalhes':str(e)})
    return resposta

@app.route('/cadastrar_jogador',methods=['POST'])# curl -X POST localhost:5000/cadastrar_jogador -d {'userid':'Spadez','senha':'123456789'} -H 'Content-Type: application/json'
def cadastrar_jogador():
    """Rota responsável por cadastrar um jogador.

    Returns:
        resposta(json): mensagem de sucesso caso tudo ocorra bem.
    """
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        jogador = Jogador(userid=dados['user'],senha=dados['senha'])
        if (jogador.userid.replace(old=' ',new='')) > 3:
            resposta = jsonify({'resultado':'user invalid'})
            return resposta
        db.session.add(jogador)
        db.session.commit()
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resposta':'erro','detalhes':str(e)})
    return resposta

@app.route('/login_jogador',methods=['POST'])# curl -X POST localhost:5000/cadastrar_jogador -d {'userid':'Spadez','senha':'123456789'} -H 'Content-Type: application/json'
def logar_jogador():
    """Realiza login de um jogador.

    Returns:
        resposta(json): Retorna sucesso e um jsonweb token caso tudo ocorra certo.
    """
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

@app.route('/login_mestre',methods=['POST'])# curl -X POST localhost:5000/login_mestre -d {'userid':'Spadez','senha':'123456789'} -H 'Content-Type: application/json'
def logar_mestre():
    """Realiza um login de mestre.

    Returns:
        resposta(json): Retorna um sucesso e um jsonweb token caso tudo ocorra bem.
    """
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
#  curl -X POST localhost:5000/criar_personagem -d {'mestreid':'Spadez','jogadorid':'Spadez','nome_do_personagem':'Ricardo','nex':'5%','forca':1,'agi':1,'int':1,'pre':1,'vig':1,'vd_max':20,'san_max':20,pe_max:10} -H 'Content-Type: application/json'
    """Realiza o cadastro de um personagem de rpg.

    Returns:
        resposta(json): Retona sucesso caso o personagem seja criado.
    """
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.get_json(force=True)
        personagem = Personagem(**dados)
        setattr(personagem, personagem.vd_atual, personagem.vd_max)
        setattr(personagem, personagem.pe_atual, personagem.pe_max) 
        setattr(personagem, personagem.san_atual, personagem.san_max)  
        inventario = Inventario(personagem=personagem.id)
        db.session.add(personagem)
        db.session.add(inventario)
        db.session.commit()
        personagem2 = db.session.query(Personagem.id).filter_by(jogadorid=dados['jogadorid']).first()
        resposta = jsonify({'resultado':'sucesso','detalhes':'id'})
    except Exception as e :
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta


@app.route('/listar/<string:identificador',methods = ['POST']) #curl -X GET localhost:5000/lista/player -d {'id':'Spadez'} -H 'Content-Type: application/json'
def listar(identificador):
    """Realiza a listagem de alguns registros.

    Args:
        identificador (string): Identifica qual é a tebela de listagem.

    Returns:
        resposta(json): Uma lista erm json com os registros.
    """
    try:
        dados = request.get_json(force=True)
        if identificador == 'player': # Caso seja um jogador chamando a função ela retornará o seu personagem.
            person = db.session.query(Personagem).filter_by(id = dados['id']).first()
            personagem = person.retorna_personagem()
            resposta = personagem
        elif identificador == 'mestre': # Caso seja um mestre a função retornará todos os jogadores da sessão.
            personagem =  db.session.query(Personagem).filter_by(mestreid = dados['id']).all()
            person_json =[ x.retorna_personagem() for x in personagem ]
            resposta = personagem
        elif identificador == 'inventario': # Retornará o inventario do jogador.
            inventario = db.session.query(Inventario).filter_by(personagem=dados['id']).all()
            itens_json =[ x.retorna_item() for x in inventario]
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

# curl -X PUT localhost:/update_personagem/simples -d{'id':'Spadez',dano_sofrido':6,'dano_mental':5} -H 'Content-Type:application/json'
@app.route('/update_persongem/<string:identificador>',methods=['PUT']) 
def update_personagem_simples(identificador):
    """Realiza o update dos dados de um personagem.

    Args:
        identificador (string): Indica o tipo de update do personagem.

    Returns:
        resposta: Retorna sucesso caso tudo ocorra certo.
    """
    if identificador == 'simples':
    # O update simples será utilizado durante as sessões, principalmente durante cenas de combate.
    # Realiza a atualização de poucos atribuitos como vida, sanidade e pontos de esforço.
        try:
            dados = request.get_json(force=True)
            personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()# Encontra o registro que sera modificado.
            if dados['dano_sofrido'] is not None:
                personagem.vd_atual = personagem.vd_atual - dados['dano_sofrido']
            if dados['cura'] is not None:
                personagem.vd_atual = personagem.vd_atual + dados['cura']
            if dados['dano_mental'] is not None:
                personagem.san_atual = personagem.san_atual - dados['dano_mental']
            if dados['san_regen'] is not None:
                personagem.san_atual = personagem.san_atual + dados['san_regen']
            if dados['pe_gasto']is not None:
                personagem.pe_atual = personagem.pe_atual - dados['pe_gasto']
            db.session.comit()
            resposta = jsonify({'resultado':'sucesso'})
        except Exception as e:
            resposta = jsonify({'resultado':'erro','detalhes':str(e)})
        return resposta
    elif identificador == 'complexo':
    # O update complexo será utilizado quando um jogador subir de nível ou receber um item que quebra os limites padrões de atributos.
    # Realiza a atualização de quase todos os atributos de um personagem.
        try:
            dados = request.json(force=True)
            personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()# Encontra o registro que sera modificado.
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

@app.route('/deletar_personagem', methods = ['DELETE'])# curl -X DELETE localhost:5000/deletar_personagem -d{'id':'Spadez'} -H 'Content-Type: application/json'
def deletar_personagem():
    """Deleta um personagem do banco de dados.

    Returns:
        resposta: Retorna sucesso caso tudo ocorra certo.
    """
    try:
        dados = request.json(force = True)
        personagem = db.session.query(Personagem).filter_by(id = dados['id']).first()
        db.session.delete(personagem)
        db.session.commit
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

@app.route('/cadastrar_item',methods=['POST']) # curl -X POST localhost:5000/ -d{'id':'Spadez','nome':'adaga','atributo':'agid20','utilidade':'dano:1d4+agi'} -H 'Content-Type: application/json'
def cadastrar_item():
    """Realiza o cadastro de um item.

    Returns:
        resposta(json): Retorna sucesso caso o item seja cadstrado.
    """
    try:
        resposta = jsonify({'resultado':'ok'})
        dados = request.json(force=True)
        inventario = db.session.query(Inventario.id).filter_by(personagem=dados['id']).first()
        item = Item(nome=dados['nome'],utilidade=['utilidade'],atributo=['atributo'], inventario = inventario)
        db.session.add(item)
        db.session.commit()
        resposta = jsonify({'resultado':'sucesso'})
    except Exception as e:
        resposta = jsonify({'resultado':'erro','detalhes':str(e)})
    return resposta

app.run(debug=True,host='0.0.0.0')