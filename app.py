import json

from flask import Flask
from flask import request
from flask import render_template
import re
import nltk
from leia import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd

from string import punctuation
from nltk import word_tokenize
from unicodedata import normalize
from sklearn.preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF

from sklearn.externals import joblib
import pickle

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/escolher_cardapio.html')
def escolherCardapio():
    nomesarq = ['prato_base1', 'prato_base2', 'prato_principal', 'guarnicao', 'salada1', 'salada2', 'salada3', 'sobremesa']
    lista = []
    try:
        for nome in nomesarq:
            arquivo = open('arquivos/' + nome + '.txt', 'r')
            conteudoarq = arquivo.read().split('\n')
            conteudoarq.sort(reverse = False)
            lista.append(conteudoarq)
    except Exception as e:
        return ''
    return render_template('escolher_cardapio.html', prato_base1 = lista[0], prato_base2 = lista[1],
    prato_principal = lista[2], guarnicao = lista[3], salada1 = lista[4], salada2 = lista[5], salada3 = lista[6],
    sobremesa = lista[7])

@app.route('/cardapio', methods=['GET', 'POST'])
def cardapioEscolhido():
    data = ''
    lista = []
    if(request.method == 'POST'):
        lista.append(request.form['pratobase1'])
        lista.append(request.form['pratobase2'])
        lista.append(request.form['pratoprincipal'])
        lista.append(request.form['guarnicao'])
        lista.append(request.form['salada1'])
        lista.append(request.form['salada2'])
        lista.append(request.form['salada3'])
        lista.append(request.form['sobremesa'])
        lista.append(request.form['picker'])
    return render_template('cardapio_do_dia.html', cardapio = lista, data = lista[len(lista)-1])

@app.route('/comentarios', methods=['GET', 'POST'])
def comentarios():
    lista = []
    lista_coments = []
    sentimento = ''
    comentarios = ''
    if(request.method == 'POST'):
        lista = request.form['card'].replace('[','').replace(']','').replace("'",'').split(',')
        comentario = request.form['txtarea']
        s = SentimentIntensityAnalyzer()
        obj_sentimento = s.polarity_scores(comentario)
        if((obj_sentimento['neg'] < obj_sentimento['pos']) or obj_sentimento['compound'] >= 0.05):
            sentimento = 'Positivo'
        elif((obj_sentimento['neg'] > obj_sentimento['pos']) or obj_sentimento['compound'] <= -0.05):
            sentimento = 'Negativo'
        elif (obj_sentimento['compound'] > -0.05) and (obj_sentimento['compound'] < 0.05):
            sentimento = 'Neutro'
    try:
        arquivo = open('arquivos/comentarios.txt', 'a+')
        if comentario != '':
            arquivo.write(comentario + '\\' + sentimento + '\n')
        arquivo.close()
        arquivo = open('arquivos/comentarios.txt', 'r')
        comentarios = arquivo.read()
        for coment in comentarios.split('\n'):
            lista_coments.append(coment.split('\\'))
        return render_template('comentarios.html', cardapio = lista, data = lista[len(lista)-1], lista_coments = lista_coments)
    except Exception as e:
        return ''
    return render_template('comentarios.html', cardapio = lista, data = lista[len(lista)-1], lista_coments = [['']])

@app.route('/cardapios')
def cardapios():
    nomesarq = ['data', 'prato_base1', 'prato_base2', 'prato_principal', 'guarnicao', 'salada1', 'salada2', 'salada3', 'sobremesa']
    lista = []
    try:
        arquivo = open('arquivos/cardapios.txt', 'r')
        cardapios = arquivo.read().split('\n')
        for cardapio in cardapios:
            lista.append(cardapio.split(';'))
        arquivo.close()
    except Exception as e:
        return ''
    return render_template('cardapios.html', cardapios = lista)
@app.route('/principal')
def principal():
    return render_template('index.html')

@app.route('/analisa_cardapio', methods=['POST'])
def api_analise():
    txt = request.form.get('txt')
    '''
        Atividade: obter a probabilidade da notícia ser sobre esporte:

        1) Preprocessar a notícia recebida (txt)
        2) Vetorizar com o mesmo TfidfVectorizer usado no dataset de treino
        3) Usar a matriz tf-idf de uma linha resultante como entrada do modelo
           Prever com predict_proba(X)[:,1]
        4) Jogar o resultado na variável "proba" (abaixo)


        Dica: para persistir um modelo treinado, usar a biblioteca joblib:

        from sklearn.externals import joblib

         Persistir
        joblib.dump(model, 'model.dat')
    '''
    linha = txt
    model = joblib.load('model.dat')
    vectorizer = joblib.load('vectorizer.dat')

    tfidf_matriz = vectorizer.transform(pd.DataFrame([[linha]])[0])

    proba = model.predict_proba(tfidf_matriz)[:,1][0]
    return json.dumps({'proba': float(proba)})

numbers = '0123456789'
stopwords = nltk.corpus.stopwords.words('portuguese')

def removeLixos(txt):
    txt = txt.lower()
    txt = ''.join([c for c in txt if c not in punctuation + numbers])
    txt = re.sub(r'\n|\r|\t', '', txt)
    txt = re.sub(r' .+? ', ' ', txt)
    txt = ' '.join([t for t in txt.split(' ') if t not in stopwords])
    return str(normalize('NFKD', txt).encode('ASCII', 'ignore')).replace('b\'','').replace('\'','')

if __name__ == '__main__':
    app.run(debug=True)
