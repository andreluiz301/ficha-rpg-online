from modelo_config_bd.modelo import *

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    m1 = Mestre(userid='jorge',senha='123456')
    j1 = Jogador(userid='roberto',senha='123')
    p1 = Personagem(mestreid='jorge',jogadorid= 'roberto',nome_do_personagem='Carlos',
                    vd_max=12,vd_atual=12,san_max=20,san_atual=20,pe_max=4,
                    pe_atual=4,forca=1,agi=1,int=3,pre=3,vig=1)
    i1 = Inventario(personagem=1)
    iten1 = Item(inventario=1,nome = 'adaga',utilidade='ataque',atributos='Dano:1d4+agi,Teste:dAgi+luta')
    db.session.add(m1)
    db.session.add(j1)
    db.session.add(p1)
    db.session.add(i1)
    db.session.add(iten1)
    db.session.commit()
    print(m1,'\n')
    print(j1,'\n')
    print(p1,'\n')
    print(i1,'\n')
    print(iten1,'\n')