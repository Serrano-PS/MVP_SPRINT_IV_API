from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Futebol, Model
from logger import logger
from schemas import *
from flask_cors import CORS
import pdb


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Ative o modo de depuração
app.debug = True

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
futebol_tag = Tag(
    name="Partidas de Futebol", description="Adição, visualização, remoção e predição de partidadas de futebol")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de partidas de futebol
@app.get('/partidas', tags=[futebol_tag],
         responses={"200": FutebolViewSchema, "404": ErrorSchema})
def get_partidas():
    """Lista todos as partidas cadastradas na base
    Retorna uma lista de partidas cadastradas na base.

    Args:
        mandante (str): mandante da partida

    Returns:
        list: lista de partidas cadastradas na base
    """
    session = Session()

    # Buscando todas as partidas
    partidas = session.query(Futebol).all()

    if not partidas:
        logger.warning("Não há partidas cadastradas na base :/")
        return {"message": "Não há partidas cadastradas na base :/"}, 404
    else:
        logger.debug(f"%d partidas econtradas" % len(partidas))
        return apresenta_partidas(partidas), 200


# Rota de adição de partida de futebol
@app.post('/partida', tags=[futebol_tag],
          responses={"200": FutebolViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: FutebolSchema):
    """Adiciona uma nova partida à base de dados
    Retorna uma representação das partidas e previsões  associados.

    Args:
        mandante (str): nome do partida
        visitante (str): visitante da partida de futebol


    Returns:
        dict: representação da partida de futebol e seu possivel resultado associado
    """

    # Carregando modelo
    ml_path = 'ml_model/model.pkl'
    modelo = Model.carrega_modelo(ml_path)
    partida = Futebol(
        mandante=form.mandante.strip(),
        visitante=form.visitante.strip(),
        mandante_ganhou=Model.preditor(modelo, form)
    )
    logger.debug(
        f"Adicionando partida de : '{partida.mandante}' x '{partida.visitante}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Adicionando partida
        session.add(partida)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(
            f"Adicionado partida de : '{partida.mandante}' x '{partida.visitante}'")

        return apresenta_partida(partida), 200

    except Exception as e:
        error_msg = f"Não foi possível salvar novo item: {str(e)}"
        logger.exception(
            f"Erro ao adicionar partida '{partida.mandante}' x x '{partida.visitante}', {error_msg}")
        return {"message": error_msg}, 400


# Métodos baseados em nome do mandante
# Rota de busca partida por nome do mandante
@app.get('/partida', tags=[futebol_tag],
         responses={"200": FutebolViewSchema, "404": ErrorSchema})
def get_partida(query: FutebolBuscaSchema):
    """Faz a busca por uma partida cadastrada na base a partir do nome do mandante

    Args:
        mandante (str): nome do mandante

    Returns:
        dict: representação da partida e seu possivel resultado associado
    """

    partida_mandante = query.mandante
    logger.debug(
        f"Coletando dados sobre partida #{partida_mandante} ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    partidas = session.query(Futebol).filter(
        Futebol.mandante == partida_mandante)

    if not partidas:
        # se o partida não foi encontrado
        error_msg = f"Partida com {partida_mandante}  não encontrada na base :/"
        logger.warning(
            f"Erro ao buscar partida do '{partida_mandante}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(
            f"Partida econtrada: '{partida_mandante}'")
        # retorna a representação das partidas
        return apresenta_partidas(partidas), 200


# Rota de remoção de partida por nome
@app.delete('/partida', tags=[futebol_tag],
            responses={"200": FutebolViewSchema, "404": ErrorSchema})
def delete_partida(query: FutebolSchema):
    """Remove um partida cadastrada na base a partir do mandante e visitante

    Args:
        mandante (str): nome do mandante
        visitante (str): nome do visitante

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    partida_mandante = unquote(query.mandante)
    partida_visitante = unquote(query.visitante)
    logger.debug(
        f"Deletando dados sobre partida #{partida_mandante} x #{partida_visitante}")

    # Criando conexão com a base
    session = Session()

    # Buscando partida
    partidas = session.query(Futebol).filter(
        (Futebol.mandante == partida_mandante) & (Futebol.visitante == partida_visitante))

    if not partidas:
        error_msg = "Partida não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar partida '{partida_mandante}' x '{partida_visitante}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        count = partidas.count()
        for partida in partidas:
            session.delete(partida)
            session.commit()
        logger.debug(
            f"Deletado #{count} partidas entre #{partida_mandante} x #{partida_visitante}")
        return {"message": f"Partidas {partida_mandante} x {partida_visitante} removidas com sucesso!"}, 200
