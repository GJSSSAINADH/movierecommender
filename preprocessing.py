import ast
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

movies=pd.read_csv("Datasets/tmdb_5000_movies.csv")
credits=pd.read_csv("Datasets/tmdb_5000_credits.csv")
credits.rename(columns={'movie_id':'id'},inplace=True)
df=pd.merge(movies,credits,on=['id','title'])
selected_features=['id','genres','keywords','overview','production_companies','title','cast','crew']
df=df[selected_features]
df.dropna(inplace=True)
def extract_genres(obj):
    li=[]
    for i in ast.literal_eval(obj):
        i['name']=i['name'].replace(' ','_')
        li.append(i['name'])
    return li
df['genres'] = df['genres'].apply(extract_genres)
def extract_keywords(obj):
    li=[]
    for i in ast.literal_eval(obj):
        i['name']=i['name'].replace(' ','_')
        li.append(i['name'])
    return li
df['keywords'] = df['keywords'].apply(extract_keywords)
def extract_cast(obj):
    li=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter<=5:
            i['name']=i['name'].replace(' ','_')
            li.append(i['name'])
            counter+=1
        else:
            break
    return li
df['cast'] = df['cast'].apply(extract_cast)
def fetch_director(obj):
    li=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            i['name']=i['name'].replace(' ','_')
            li.append(i['name'])
            return li
    return np.nan
df['crew'] = df['crew'].apply(fetch_director)
def string_to_list(obj):
    li=[]
    obj=obj.replace(' ','_')
    li.append(obj)
    return li
title=df['title'].apply(string_to_list)
df.rename(columns={'crew':'director'},inplace=True)
def extract_companies(obj):
    li=[]
    for i in ast.literal_eval(obj):
        i['name']=i['name'].replace(' ','_')
        li.append(i['name'])
    return li
df['production_companies'] = df['production_companies'].apply(extract_companies)
df['overview'] = df['overview'].apply(lambda x: x.split())
df.dropna(inplace=True)
df['tags']=df['genres']+df['keywords']+df['cast']+df['production_companies']+df['overview']+df['director']+title
new_movies=df[['id','title','tags']]
new_movies['tags']=new_movies['tags'].apply(lambda x: ' '.join(x))
new_movies['tags']=new_movies['tags'].apply(lambda x: x.lower())
cv=CountVectorizer(max_features=5000 ,stop_words='english')
new_movies_matrix=cv.fit_transform(new_movies['tags'])
ps= PorterStemmer()
def stemming(obj):
    li=[]
    for i in obj.split():
        li.append(ps.stem(i))
    return " ".join(li)
new_movies['tags']=new_movies['tags'].apply(stemming)
similarity_matrix = cosine_similarity(new_movies_matrix)

def import_dataframes():
    return [new_movies,similarity_matrix]

