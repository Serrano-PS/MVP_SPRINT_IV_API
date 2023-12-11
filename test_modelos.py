from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model
from model.preprocessador import PreProcessador
from sklearn.preprocessing import LabelEncoder
import numpy as np

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
pre_processador = PreProcessador()

# Parâmetros
url_dados = "database/campeonato-brasileiro-golden.csv"
colunas = ['mandante', 'visitante', 'mandante_ganhou']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Instancia um objeto LabelEncoder para codificar as categorias em números
le = LabelEncoder()

# Aplica a codificação aos dados da coluna 'mandante' no dataset
dataset['mandante'] = le.fit_transform(dataset['mandante'])

# Aplica a codificação aos dados da coluna 'visitante' no dataset
dataset['visitante'] = le.fit_transform(dataset['visitante'])

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]
Y = np.nan_to_num(Y, nan=0)
# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"

# Pré-processar dados
X_train, X_test, Y_train, Y_test = pre_processador.pre_processar(
    dataset, percentual_teste=0.9, seed=777)


# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = 'ml_model/model.pkl'
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(
        modelo_knn, X_train, Y_train)

    # Testando as métricas do KNN
    assert acuracia_knn >= 0.6
    assert recall_knn >= 0.55
    assert precisao_knn >= 0.55
    assert f1_knn >= 0.7
