from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [

    path('', views.home, name='home'),
    path('charts/user-review/', views.UserReviewChartView.as_view(), name='chart-users'),
    path('charts/genre/', views.GenreChartView.as_view(), name='chart-genre'),
    path('charts/anime-review/', views.AnimeReviewChartView.as_view(), name='chart-anime'),
    path('anime/new/', views.newAnime, name='new-anime')
]
