from pydantic import BaseModel
from typing import Optional, List
from model.futebol import Futebol
import json
import numpy as np


class FutebolSchema(BaseModel):
    """ Define como uma partida a ser inserido deve ser representado
    """
    mandante: str = "Vasco"
    visitante: str = "Flamengo"


class FutebolViewSchema(BaseModel):
    """Define como uma partida de futebol será retornado
    """
    id: int = 1
    mandante: str = "Vasco"
    visitante: str = "Flamengo"
    mandante_ganhou: int = None


class FutebolBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do mandante.
    """
    mandante: str = "Vasco"


class ListaFutebolSchema(BaseModel):
    """Define como uma lista de partidas de futebol será representada
    """
    futebol: List[FutebolSchema]


class FutebolDelSchema(BaseModel):
    """Define como uma partida de futebol para deleção será representado
    """
    mandante: str = "Vasco"


def apresenta_partida(futebol: Futebol):
    """ Retorna uma representação de uma partida de futebol seguindo o schema definido em
        FutebolViewSchema.
    """
    return {
        "id": futebol.id,
        "mandante": futebol.mandante,
        "visitante": futebol.visitante,
        "mandante_ganhou": futebol.mandante_ganhou
    }

# Apresenta uma lista de partidas


def apresenta_partidas(futebol: List[Futebol]):
    """ Retorna uma representação de todas as partida de futebol seguindo o schema definido em
       FutebolViewSchema.
    """
    result = []
    for partida in futebol:
        result.append({
            "mandante": partida.mandante,
            "visitante": partida.visitante,
            "mandante_ganhou": partida.mandante_ganhou
        })

    return {"futebol": result}
