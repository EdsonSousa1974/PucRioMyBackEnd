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
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a pessoa e as movimentações financeiras.
    # Essa relação é implicita, não está salva na tabela 'pessoa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    #aki comentarios = relationship("Comentario")

    def __init__(self, cpf:str, nome:str, telefone:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Pessoa

        Arguments:
            cpf: cpf da pessoa.
            nome: nome da pessoa.
            telefone: telefone da pessoa.
            data_insercao: data de quando a pessoa foi inserida na base
        """
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
            