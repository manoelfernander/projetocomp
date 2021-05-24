import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer


filmes = pd.read_csv("movies_metadata.csv")
creditos = pd.read_csv("credits.csv")
palavraschaves = pd.read_csv("keywords.csv")


filmes = filmes[["id", "title", "genres"]]

# Função de limpar os ID's

def limpa_id(x):
    try:
        return int(x)

    except:
        return np.nan



filmes['id'] = filmes['id'].apply(limpa_id)
filmes = filmes[filmes['id'].notnull()]


filmes['id'] = filmes['id'].astype('int')
palavraschaves['id'] = palavraschaves['id']
creditos['id'] = creditos['id'].astype('int')


# Juntando através do id

filmes1 = filmes.merge(creditos, on="id")
filmes2 = filmes1.merge(palavraschaves, on="id")


# aplicando literal_eval para fazer string -> objetos.

filmes2['genres'] = filmes2['genres'].apply(literal_eval)
filmes2['cast'] = filmes2['cast'].apply(literal_eval)
filmes2['crew'] = filmes2['crew'].apply(literal_eval)
filmes2['keywords'] = filmes2['keywords'].apply(literal_eval)



# pegando o nome dos generos associados
filmes2['crew'] = filmes2['crew'].apply(lambda x: [i['name'].lower() for i in x if i['job'] == 'Director'])


# juntando com as palavras chaves

df = filmes2


#print(df.head())

df["genres"] = df["genres"].apply(lambda x: [i["name"].lower() for i in x])
df["cast"] = df["cast"].apply(lambda x: [i["name"].lower() for i in x])
df["keywords"] = df["keywords"].apply(lambda x: [i["name"].lower() for i in x])



#pegando até 3 caracteristicas de cada filme
# se pegarmos muitas caracteristicas pode aumentar demais a complexidade do algortimo

df["genres"] = df["genres"].apply(lambda x: x[:3] if len(x)>3 else x)
df["cast"] = df["cast"].apply(lambda x: x[:3] if len(x)>3 else x)
df["keywords"] = df["keywords"].apply(lambda x: x[:3] if len(x)>3 else x)


#removendo os espaços

df["cast"] = df["cast"].apply(lambda x: [i.replace(" ","") for i in x])
df["crew"] = df["crew"].apply(lambda x: [i.replace(" ","") for i in x])
df["keywords"] = df["keywords"].apply(lambda x: [i.replace(" ","") for i in x])
df["genres"] = df["genres"].apply(lambda x: [i.replace(" ","") for i in x])




#Transformando tudo em uma coluna só

df["metadata"] = df.apply(lambda x : " ".join(x["genres"]) + " "  + " ".join(x["cast"]) + " " + " ".join(x["crew"]) + " " + " ".join(x["keywords"]), axis = 1)

df_metadata = df.iloc[:5000, 6]



#Usando cosseno de similaridade para achar a semelhança entre dois filmes

cv = CountVectorizer(stop_words = 'english')

contador_matrix = cv.fit_transform(df_metadata)

cosseno_sim_matrix = cosine_similarity(contador_matrix)


#Mapeando a função

mapear = pd.Series(df_metadata.index, index = df.iloc[:5000, 1])



# Funcao de recomendacao de acordo com nossos metadados

def sistema(filmes_input):
    filme_indexado = mapear[filmes_input]

    # obtendo os valores similares

    score = list(enumerate(cosseno_sim_matrix[filme_indexado]))

    score = sorted(score, key=lambda x: x[1], reverse=True)

    # Amostra de 20 filmes

    score = score[1:20]

    indices = [i[0] for i in score]

    return (mapear.iloc[indices])


def sistema2(filmes_input):
    # "Somando os filmes"
    #indice depende do tamanho do dataframe
    indice = 20000
    df_metadata[indice] = ' '
    for filme in filmes_input:
        df_metadata[indice] += ' ' + df_metadata[mapear[filme]]

    # Usando a similaridade de cosseno
    cv = CountVectorizer(stop_words='english')
    contador_matrix = cv.fit_transform(df_metadata)
    cosseno_sim_matrix = cosine_similarity(contador_matrix)

    # Resetando a soma de filmes
    df_metadata[indice] = ' '

    # obtendo os valores similares

    score = list(enumerate(cosseno_sim_matrix[indice]))
    score = sorted(score, key=lambda x: x[1], reverse=True)

    # Amostra de 20 filmes

    n_filmes = len(filmes_input)
    score = score[(n_filmes + 1):20]
    indices = [i[0] for i in score]

    # return (score)
    return (mapear.iloc[indices])


#Aplicar filtro de filmes mais relevantes