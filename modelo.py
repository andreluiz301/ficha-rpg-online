from config import db

class Mestre(db.Model):
    user = db.Column(db.String(254),primary_key=True)
    senha = db.String(db.String(254))

    def __str__(self):
        s = self.user
        return s

class Jogador(db.Model):
    user = db.Column(db.String(254),primary_key=True)
    senha = db.String(db.String(254))

    def __str__(self):
        s = self.user
        return s


class Personagem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    mestreid = db.Column(db.String(254),db.ForeignKey(Mestre.user),nullable = False) # Utilizado para reconhecer a qual mesa pertence o personagem.
    jogadorid = db.Column(db.String(254),db.ForeignKey(Mestre.user),nullable = False) # Utilizado para reconhecer o jogador que criou o personagem.
    nome_do_personagem = db.Column(db.String(254))
    vida_max = db.Column(db.Integer)
    sanidade_max = db.Column(db.Integer)
    pe_max = db.Column(db.Integer) #Pontos de esforço.
    forca = db.Column(db.Integer)
    agilidade = db.Column(db.Integer)
    intelecto = db.Column(db.Integer) 
    presenca = db.Column(db.Integer) # Capacidade de socialização ou percepção do ambiente.
    vigor = db.Column(db.Integer)   # Resistência física 

    def retorna_personagem(self):
        personagem = {
            'nome':self.nome,
            'vida':self.vida,
            'sanidade':self.sanidade,
            'pe':self.pe,
            'idade':self.idade,
            'forca':self.forca,
            'agilidade':self.agilidade,
            'intelecto':self.intelecto,
            'presença':self.presenca,
            'vigor':self.vigor
        }
        return personagem
    
    def __str__(self):
        s = (self.nome_do_personagem,self.idade,self.sanidade,self.pe,self.forca,
                        self.agilidade,self.intelecto,self.presenca,self.vigor)
        return s

class Ficha(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    ficha_path = db.Column(db.Text)
    personagem = db.Column(db.String(254),db.ForeignKey(Personagem.id),nullable = False)

    def retorna_ficha(self):
        ficha_path = self.ficha_path
        return ficha_path

class  Inventario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    personagem = db.Column(db.String(254),db.ForeignKey(Personagem.id),nullable = False)

    def retorna_inventario(self):
        inventario = self.itens
        return inventario

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    inventario = db.Column(db.String(254),db.ForeignKey(Inventario.id),nullable = False)
    item = db.relationship('Item', backref='Inventario',)
    nome = db.Column(db.String(254))
    utilidade = db.Column(db.String(254))
    atributos = db.Column(db.String(254))

    def __str__(self):
        item = f'{self.nome},{self.utilidade},{self.atributos}'
        return item
