from django.shortcuts import redirect, render
import requests
from preprocessing import import_dataframes


# Create your views here.
def index(request):
    df=import_dataframes()[0]
    movies_dict=df.to_dict()
    context={}
    context['list']=[]
    for i in range(len(movies_dict['title'])):
        try:
            context['list'].append([movies_dict['title'][i],i])
        except:
            pass

    if request.method =='POST':
        movie_name=request.POST.get('movie')
        return redirect('getrecommendations',movie_name)
    return render(request, 'index.html', context)

def getrecommendations(request,movie_name):
    df=import_dataframes()[0]
    similarity=import_dataframes()[1]
    movie_index=df[df['title']==movie_name].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),key=lambda x:x[1],reverse=True)
    recommended_movies=[]
    for i in movie_list[1:9]:
        recommended_movies.append(df.iloc[i[0]].id)
    movie_id=df.loc[df['title']==movie_name].id.values[0]
    res=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7a02116281ca42a351c8ad4f950ae04d'.format(movie_id))
    context={}
    context['recommended_movies']=[]
    for i in recommended_movies:
        context['recommended_movies'].append(fetch_name_poster(i))
    context['movie_name']=movie_name
    context['ratings']=fetch_rating(res)
    context['backdrop']=fetch_backdrop(res)
    context['overview']=fetch_overview(res)
    res.close()

    return render(request,'recommendations.html',context)

def fetch_name_poster(movie_id):
    res=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7a02116281ca42a351c8ad4f950ae04d'.format(movie_id))
    data=res.json()
    res.close
    return ['https://image.tmdb.org/t/p/w500{}'.format(data['poster_path']),data['title']]

def fetch_backdrop(res):
    data=res.json()
    return 'https://image.tmdb.org/t/p/w1280{}'.format(data['backdrop_path'])

def fetch_overview(res):
    data=res.json()
    return data['overview']

def fetch_rating(res):
    data=res.json()
    return data['vote_average']
