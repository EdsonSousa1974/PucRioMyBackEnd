from pydantic import BaseModel
from typing import Optional, List
from model.pessoa import Pessoa

class PessoaSchema(BaseModel):
    """ Define como uma nova pessoa a ser inserida deve ser representada
    """
    cpf: str = "12345678901"
    nome: str = "Edson Sousa"
    telefone: str = "21984483515"
    cep: str = "25540260"
    bairro: str = "Coelho da Rocha"
    cidade: str = "São João de Meriti"
    uf: str = "RJ"


class PessoaBuscaPorNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
    
    Que será feita apenas com base no nome da pessoa.
    """
    nome: str = "Nome para ser buscado"


class ListagemPessoasSchema(BaseModel):
    """ Define como uma listagem de pessoas será retornada.
    """
    pessoa:List[PessoaSchema]


def apresenta_pessoas(pessoas: List[Pessoa]):
    """ Retorna uma representação da pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for pessoa in pessoas:
        result.append({
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "telefone": pessoa.telefone,
            "cep": pessoa.cep,
            "bairro": pessoa.bairro,
            "cidade": pessoa.cidade,
            "uf": pessoa.uf,            
        })

    return {"pessoas": result}


class PessoaViewSchema(BaseModel):
    """ Define como uma pessoa será retornada: pessoa.
    """
    id: int = 1
    cpf: str = "12345678901"
    nome: str = "Edson Sousa"
    telefone: str = "21984483515"
    cep: str = "25540260"
    bairro: str = "Coelho da Rocha"
    cidade: str = "São João de Meriti"
    uf: str = "RJ"


class PessoaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_pessoa(pessoa: Pessoa):
    """ Retorna uma representação da pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": pessoa.id,
        "cpf": pessoa.cpf,
        "nome": pessoa.nome,
        "telefone": pessoa.telefone,
        "cep": pessoa.cep,
        "bairro": pessoa.bairro,
        "cidade": pessoa.cidade,
        "uf": pessoa.uf,            
    }

class PessoaBuscaPorCEPSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. 
    
    Que será feita apenas com base no CEP da pessoa.
    """
    cep: str = "CEP para ser buscado"

def apresenta_cep(pessoa: Pessoa):
    """ Retorna uma representação do cep seguindo o schema definido em
        CepViewSchema.
    """
    return {
        "cep": pessoa.cep,
        "bairro": pessoa.bairro,
        "cidade": pessoa.cidade,
        "uf": pessoa.uf,            
    }
