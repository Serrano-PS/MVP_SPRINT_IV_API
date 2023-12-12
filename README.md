# MVP_SPRINT_IV_API

## **Modelo de Previsão de Resultados de Jogos de Futebol**

Este projeto consiste em um modelo de aprendizado de máquina desenvolvido para prever os resultados de jogos de futebol, considerando o time mandante e o adversário. O projeto está dividido em duas partes distintas: a API  e o Front-end.

## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Google Colab

https://colab.research.google.com/drive/1kGG5FkHhuDN1B3XZh3kr1J8PZTvHMflj?usp=sharing
