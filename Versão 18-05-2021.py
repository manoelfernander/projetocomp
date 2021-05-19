#!/usr/bin/env python
# coding: utf-8

# In[1]:



import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer


# In[2]:


filmes = pd.read_csv("movies_metadata.csv")
creditos = pd.read_csv("credits.csv")

#Usando as palavras chaves no dataset keywords

palavraschaves = pd.read_csv("keywords.csv")


# In[3]:


filmes.head()


# In[4]:


filmes = filmes[["id", "title", "genres"]]


# In[5]:


#Função de limpar os ID's

def limpa_id(x):
    
    
    try: 
        
        return int(x)
    
    except:
        
        
        return np.nan
    
    


# In[6]:


filmes.head()


# In[7]:


filmes['id'] = filmes['id'].apply(limpa_id)
filmes = filmes[filmes['id'].notnull()]


# In[8]:


filmes['id'] = filmes['id'].astype('int')
palavraschaves['id'] = palavraschaves['id']
creditos['id'] = creditos['id'].astype('int')


# In[9]:


#Juntando através do id

filmes1 = filmes.merge(creditos, on = "id")
filmes2 = filmes1.merge(palavraschaves, on = "id")


# In[10]:


filmes.head()


# In[11]:


filmes1.head()


# In[12]:


filmes2.head()


# In[13]:


creditos.head()


# In[14]:


# aplicando literal_eval para fazer string -> objetos.

filmes2['genres'] = filmes2['genres'].apply(literal_eval)


# In[15]:


filmes2.head()


# In[17]:


filmes2.info()


# In[18]:


filmes2['cast'] = filmes2['cast'].apply(literal_eval)


# In[19]:


filmes2['crew'] = filmes2['crew'].apply(literal_eval)
filmes2['keywords'] = filmes2['keywords'].apply(literal_eval)


# In[20]:


#pegando o nome dos generos associados
filmes2['crew'] = filmes2['crew'].apply(lambda x: [i['name'].lower() for i in x if i['job'] == 'Director'])


# In[25]:


#juntando com as palavras chaves
df = filmes2


# In[26]:


df.head()


# In[2]:


df["genres"] = df["genres"].apply(lambda x: [i["name"].lower() for i in x])


# In[3]:


df.head()


# In[4]:


df["cast"] = df["cast"].apply(lambda x: [i["name"].lower() for i in x])


# In[6]:


df["keywords"] = df["keywords"].apply(lambda x: [i["name"].lower() for i in x])


# In[7]:


#pegando até 3 caracteristicas de cada filme
# se pegarmos muitas caracteristicas pode aumentar demais a complexidade do algortimo

df["genre"] = df["genres"].apply(lambda x: x[:3] if len(x)>3 else x)
df["cast"] = df["cast"].apply(lambda x: x[:3] if len(x)>3 else x)
df["keywords"] = df["keywords"].apply(lambda x: x[:3] if len(x)>3 else x)


# In[ ]:





# In[9]:


df.head()


# In[11]:


df = df[['id', 'title', 'genres', 'cast', 'crew', 'keywords']]


# In[12]:


df.head()


# In[16]:


#removendo os espaços

df["cast"] = df["cast"].apply(lambda x: [i.replace(" ","") for i in x])
df["crew"] = df["crew"].apply(lambda x: [i.replace(" ","") for i in x])
df["keywords"] = df["keywords"].apply(lambda x: [i.replace(" ","") for i in x])
df["genres"] = df["genres"].apply(lambda x: [i.replace(" ","") for i in x])


# In[17]:


df.head()


# In[19]:


#Transformando tudo em uma coluna só 

df["metadata"] = df.apply(lambda x : " ".join(x["genres"]) + " "  + " ".join(x["cast"]) + " " + " ".join(x["crew"]) + " " + " ".join(x["keywords"]), axis = 1)


# In[20]:


df.head()


# In[24]:


df.info()


# In[39]:


df_metadata = df.iloc[1:4000, 6]


# In[40]:


df_metadata


# In[41]:


#Usando cosseno de similaridade para achar a semelhança entre dois filmes

cv = CountVectorizer(stop_words = 'english')

contador_matrix = cv.fit_transform(df_metadata)

cosseno_sim_matrix = cosine_similarity(contador_matrix)


# In[42]:


cosseno_sim_matrix


# In[44]:


len(cosseno_sim_matrix)


# In[47]:


#Mapeando a função 

mapear = pd.Series(df_metadata.index, index = df.iloc[1:4000, 1])
mapear


# In[48]:


df_metadata


# In[57]:


# Funcao de recomendacao de acordo com nossos metadados

def sistema(filmes_input):
    
    filme_indexado = mapear[filmes_input]
    
    #obtendo os valores similares
    
    score = list(enumerate (cosseno_sim_matrix[filme_indexado]))
    
    score = sorted(score, key = lambda x: x[1], reverse = True)
    
    # Amostra de 20 filmes
    
    
    score = score[1:20]
    
    indices = [i[0] for i in score]
    
    return (mapear.iloc[indices])


# In[58]:


sistema("Frisk")


# In[ ]:




