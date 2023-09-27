from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column("pk_pessoa", Integer, primary_key=True)
    cpf = Column(String(11), unique=True)
    nome = Column(String(140))
    telefone = Column(String(25))
    cep = Column(String(8))
    bairro = Column(String(35))
    cidade = Column(String(35))
    uf = Column(String(2))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a pessoa e as movimentações financeiras.
    # Essa relação é implicita, não está salva na tabela 'pessoa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    #aki comentarios = relationship("Comentario")

    def __init__(self, cpf:str, nome:str, telefone:str, cep:str, bairro:str, cidade:str, uf:str, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Pessoa

        Arguments:
            cpf: cpf da pessoa.
            nome: nome da pessoa.
            telefone: telefone da pessoa.
            cep: cep domiciliar da pessoa.
            bairro: bairro domiciliar da pessoa.
            cidade: cidade domiciliar da pessoa.
            uf: uf domiciliar da pessoa.
            data_insercao: data de quando a pessoa foi inserida na base
        """
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.cep = cep
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
            