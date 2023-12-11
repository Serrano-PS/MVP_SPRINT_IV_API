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

        # # Cria o DataFrame de entrada
        # data = {'mandante':  [mandante_index],
        #         'visitante': [visitante_index]
        #         }

        # atributos = ['mandante', 'visitante']
        # entrada = pd.DataFrame(data, columns=atributos)

        # array_entrada = entrada.values
        # # Seleciona as colunas desejadas e converte para o tipo int
        # X_entrada = array_entrada[:, 0:2].astype(int)

        # # Cria um StandardScaler e ajusta aos dados de entrada
        # scaler = StandardScaler()
        # scaler.fit(X_entrada)

        # # Padronização nos dados de entrada usando o scaler
        # rescaled_entrada_X = scaler.transform(X_entrada)

        # # Realiza a previsão com o modelo treinado
        # vencedor = model.predict(rescaled_entrada_X)

        # return int(vencedor[0])
