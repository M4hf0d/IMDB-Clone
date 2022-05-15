from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (ReviewList, ReviewDetails, ReviewCreate,
                                     ApiOverviewAV,
                                     WatchListSV, StreamPlatformSV)


router = DefaultRouter()
router.register('platforms', StreamPlatformSV, basename='streamplatform')
router.register('list', WatchListSV, basename='watchlist')
urlpatterns = [

    path("", ApiOverviewAV.as_view(), name='Overview'),
    path('', include(router.urls)),
    # path("list/", WatchListAV.as_view(), name='list'),
    # path("list/<int:pk>/", WatchListDetailsAV.as_view(), name='WatchList_details'),


    path('', include(router.urls)),
    # path("platforms/", StreamPlatformAV.as_view(), name='list platforms'),
    # path("platforms/<int:pk>/", StreamPlatformDetailsAV.as_view(),
    #      name='platform details'),

    path("platforms/<int:pk>/review",
         ReviewCreate.as_view(), name='review-create'),
    path("platforms/<int:pk>/review", ReviewList.as_view(), name='review-list'),
    path("platforms/review/<int:pk>",
         ReviewDetails.as_view(), name='review-details'),

    # path("review/", ReviewList.as_view(), name='list Reviews'),
    # path("review/<int:pk>/",ReviewDetails.as_view(), name='reviews details'),
]
