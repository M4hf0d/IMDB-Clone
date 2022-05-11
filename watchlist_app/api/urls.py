from django.urls import path,include
from watchlist_app.api.views import MovieListAV, MovieDetailsAV,MovieListOrderedAV

urlpatterns =[
    path("list/",MovieListAV.as_view(), name='list'),
    path("list/<str:order>/",MovieListOrderedAV.as_view(), name='list ordered by <str order>'),
    path("<int:pk>/",MovieDetailsAV.as_view(), name='movie_details'),

]

