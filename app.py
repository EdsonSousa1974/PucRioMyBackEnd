import requests
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Pessoa #aqui, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

from schemas.pessoa import PessoaBuscaPorCEPSchema

info = Info(title="Meu cadastro Pessoal", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag   = Tag(name="Documentação", description="Documentação feita com Swagger")
pessoa_tag = Tag(name="Pessoa", description="Adição, visualização e remoção de uma pessoa na base")
cep_tag    = Tag(name="CEP", description="Busca do CEP digitado via microserviço")
#movimento_tag = Tag(name="Movimento", description="Adição de um valor de débito ou crédito para pessoa cadastrada na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/pessoa', tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pessoa(form: PessoaSchema):
    """Adiciona uma pessoa na base de dados

    Retorna uma representação das pessoal.
    """
    pessoa = Pessoa(
        nome=form.nome,
        telefone=form.telefone,
        cpf=form.cpf,
        cep=form.cep,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf)
    logger.debug(f"Adicionando pessoa de nome: '{pessoa.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pessoa
        session.add(pessoa)
        # efetivando o camando de adição de nova pessoa na tabela
        session.commit()
        logger.debug(f"Adicionado pessoa de nome: '{pessoa.nome}'")
        return apresenta_pessoa(pessoa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pessoa com o mesmo cpf já salvo na base :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova pessoa :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/pessoas', tags=[pessoa_tag],
         responses={"200": ListagemPessoasSchema, "404": ErrorSchema})
def get_pessoas():
    """Faz a busca por todas as pessoas cadastradas

    Retorna uma representação da listagem de pessoas.
    """
    logger.debug(f"Coletando pessoas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        # se não há pessoas cadastradas
        return {"pessoas": []}, 200
    else:
        logger.debug(f"%d pessoas encontradas" % len(pessoas))
        # retorna a representação de pessoa
        print(pessoas)
        return apresenta_pessoas(pessoas), 200


@app.get('/pessoa', tags=[pessoa_tag],
         responses={"200": PessoaBuscaPorNomeSchema, "404": ErrorSchema})
def get_pessoa(query: PessoaBuscaPorNomeSchema):
    """Faz a busca por uma pessoa a partir do nome

    Retorna uma representação das pessoas e seus movimentos associados.
    """
    pessoa_nome = query.nome
    logger.debug(f"Coletando dados sobre pessoa #{pessoa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa = session.query(Pessoa).filter(Pessoa.nome == pessoa_nome).first()

    if not pessoa:
        # se a pessoa não foi encontrada
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"Erro ao buscar pessoa '{pessoa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa encontrado: '{pessoa.nome}'")
        # retorna a representação da pessoa
        return apresenta_pessoa(pessoa), 200


@app.delete('/pessoa', tags=[pessoa_tag],
            responses={"200": PessoaDelSchema, "404": ErrorSchema})
def del_pessoa(query: PessoaBuscaPorNomeSchema):
    """Deleta uma Pessoa a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    pessoa_nome = unquote(unquote(query.nome))
    print(pessoa_nome)
    logger.debug(f"Deletando dados sobre a pessoa #{pessoa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pessoa).filter(Pessoa.nome == pessoa_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pessoa #{pessoa_nome}")
        return {"mesage": "Pessoa removida", "id": pessoa_nome}
    else:
        # se a pessoa não foi encontrada
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"Erro ao deletar pessoa #'{pessoa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


#busca cep
@app.get('/cep', tags=[cep_tag],
         responses={"200": PessoaBuscaPorCEPSchema, "404": ErrorSchema})

def get_cep(query: PessoaBuscaPorCEPSchema):
    """Faz a busca por CEP

    Retorna uma lista com bairro, cidade e UF.
    """
    cep = query.cep

    cep = cep.replace("-", "").replace(".", "").replace(" ", "")

    if len(cep) == 8:
        link = f'https://viacep.com.br/ws/{cep}/json/'

        requisicao = requests.get(link)

        dic_requisicao = requisicao.json()

        logger.debug(f"CEP encontrado: '{cep}'")
        # retorna a representação do cep
        return dic_requisicao, 200

    else:
        # se o CEP não conter 8 números
        error_msg = "CEP Inválido :/"
        logger.warning(f"Erro ao buscar CEP '{cep}', {error_msg}")
        return {"mesage": error_msg}, 404
