from config import db

class Mestre(db.Model):
    user = db.Column(db.String(254),primary_key=True)
    senha = db.String(db.String(254))


class Personagem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    mestreid = db.Column(db.String(254),db.ForeignKey(Mestre.user),nullable = False) # Utilizado para reconhecer a qual mesa pertence o personagem
    user = db.Column(db.String(254)) # Utilizado para login.
    senha = db.String(db.String(254)) # Utilizado para login.
    nome_do_personagem = db.Column(db.String(254))
    idade = db.Column(db.Integer)
    vida = db.Column(db.Integer)
    sanidade = db.Column(db.Integer)
    pe = db.Column(db.Integer) #Pontos de esforço.
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



