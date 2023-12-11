import numpy as np
import pandas as pd
import pickle
import joblib
import pdb
from sklearn.preprocessing import StandardScaler
from sklearn.tree import export_text


class Model:

    def carrega_modelo(path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """

        if path.endswith('.pkl'):
            model = pickle.load(open(path, 'rb'))
        elif path.endswith('.joblib'):
            model = joblib.load(path)
        else:
            raise Exception('Formato de arquivo não suportado')
        return model

    @staticmethod
    def preditor(model, form):
        """Realiza a predição da possibilidade do mandante ganhar o jogo ou não com base no modelo treinado
        """

        # Lista de equipes
        lista_equipes = ["America-MG", "America-RN", "Athletico-PR", "Atletico-GO", "Atletico-MG", "Avai", "Bahia", "Barueri", "Botafogo-RJ", "Bragantino", "Brasiliense", "Ceara", "Chapecoense", "Corinthians", "Coritiba", "Criciuma",
                         "Cruzeiro", "CSA", "Cuiaba", "Figueirense", "Flamengo", "Fluminense", "Fortaleza", "Goias", "Gremio", "Gremio Prudente", "Guarani", "Internacional", "Ipatinga", "Joinville", "Juventude", "Nautico",
                         "Palmeiras", "Parana", "Paysandu", "Ponte Preta", "Portuguesa", "Santa Cruz", "Santo Andre", "Santos", "Sao Caetano", "Sao Paulo", "Sport", "Vasco", "Vitoria"]

        # Cria os índices dos times mandante e visitante
        mandante_index = lista_equipes.index(form.mandante)
        visitante_index = lista_equipes.index(form.visitante)

        X_input = np.array([mandante_index,
                            visitante_index,
                            ])

        # Faremos o reshape para que o modelo entenda que estamos passando
        vencendor = model.predict(X_input.reshape(1, -1))
        return int(vencendor[0])
