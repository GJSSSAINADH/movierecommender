from django.urls import path
import recommender.views

urlpatterns = [
    path('', recommender.views.index, name='index'),
    path('getrecommendations/<str:movie_name>', recommender.views.getrecommendations, name='getrecommendations'),
]