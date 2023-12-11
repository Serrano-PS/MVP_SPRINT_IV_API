from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = mandante,visitante,mandante_ganhou


class Futebol(Base):
    __tablename__ = 'futebol'

    id = Column(Integer, primary_key=True)
    mandante = Column("mandante", String[50])
    visitante = Column("visitante",  String[50])
    mandante_ganhou = Column("mandante_ganhou", Integer, nullable=False)

    def __init__(self, mandante: str, visitante: str, mandante_ganhou: int):
        """
        Cria um Jogo de futebol

        Arguments:
        mandante: time mandante
            visitante: time mandante
            mandante_ganhou: mandante ganhará o jogo?
        """
        self.mandante = mandante
        self.visitante = visitante
        self.mandante_ganhou = mandante_ganhou
