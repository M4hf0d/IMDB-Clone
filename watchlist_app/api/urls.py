from django.urls import path,include
from watchlist_app.api.views import WatchListAV, WatchListDetailsAV, ApiOverviewAV,StreamPlatformAV,StreamPlatformDetailsAV

urlpatterns =[
    path("",ApiOverviewAV.as_view(), name='Overview'),    
    path("list/",WatchListAV.as_view(), name='list'),
    path("list/<int:pk>/",WatchListDetailsAV.as_view(), name='WatchList_details'),
    path("platforms/",StreamPlatformAV.as_view(), name='list platforms'),
    path("platforms/<int:pk>/",StreamPlatformDetailsAV.as_view(), name='platform details'),

]

