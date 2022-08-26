from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..models import Review, WatchList, StreamPlatform
from watchlist_app.models import WatchList
from watchlist_app.api.serializers import *
from .permissions import *
from .throttling import *
from .pagination import WatchListPagination

fields = [field.name for field in WatchList._meta.get_fields()]

# fields =["id", "name", "description" ,"active"]


class ApiOverviewAV(APIView):

    def get(self, request):
        print(fields)
        api_urls = {
            'List': 'http://127.0.0.1:8000/list/',
            'List platforms': 'http://127.0.0.1:8000/platforms/',
            'Add Review': 'http://127.0.0.1:8000/platforms/review/'

        }
        return Response(api_urls)


class ReviewCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]


    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')  # got the pk from the request
        movie = WatchList.objects.get(pk=pk)  # selected the movie to review

        ruser = self.request.user
        review_queryset = Review.objects.filter(
            review_user=ruser, watchlist=movie)
        if review_queryset.exists():
            raise ValidationError("You already reviewed this show")
        # saved the review to the movies

        if movie.n_ratings == 0 :
            movie.avg_ratings = serializer.validated_data['rating']
        else : 
            sum = 0
            for rating in Review.objects.filter(watchlist=pk) :
                sum = sum + rating.rating
            movie.avg_ratings = sum / movie.n_ratings
            
        movie.n_ratings = movie.n_ratings + 1
        movie.save()
        serializer.save(watchlist=movie, review_user=ruser)


class ReviewList(generics.ListAPIView): #all the reviews of the pk show
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUser_AdminOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "review-detail"  




class WatchListSV(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    permission_classes = [AdminOrReadOnlyPermission]
    def get_serializer_class(self):
       if self.request.method == 'POST':
           return WatchListSerializer
       return WatchListlSerializer
    pagination_class = WatchListPagination


class StreamPlatformSV(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnlyPermission]

class MovieList(generics.ListAPIView): #all the reviews of the pk show
    serializer_class = WatchListlSerializer
    queryset = WatchList.objects.all()
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]
    filter_backends = [filters.SearchFilter]
    search_fields  = ['title', 'platform__name']
    pagination_class = WatchListPagination
    


#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class WatchListAV(APIView):
#     def get(self, request):
#         try:
#             order = str(request.query_params["orderby"])
#             if order in fields:
#                 Movies = WatchList.objects.all().order_by(order)
#             serializer = WatchListSerializer(Movies, many=True)
#         except:
#             Movie = WatchList.objects.all().order_by("id")  # default
#             serializer = WatchListSerializer(Movie, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class WatchListDetailsAV (APIView):
#     def get(self, request, pk):
#         try:
#             Movies = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error': 'WatchList does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(Movies)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         Movies = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(Movies, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         Movies = WatchList.objects.get(pk=pk)
#         Movies.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class StreamPlatformAV(APIView):
#     def get(self, request):
#         Platforms = StreamPlatform.objects.all()  # default
#         serializer = StreamPlatformSerializer(
#             Platforms, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# class StreamPlatformDetailsAV(APIView):
#     def get(self, request, pk):
#         try:
#             platforms = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'Platform does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(platforms)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def WatchList_list (request):
#     if request.method == 'GET' :
#         WatchLists = WatchList.objects.all()
#         serializer = WatchListSerializer(WatchLists, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST' :
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def WatchList_details (request,pk):
#     if request.method == 'GET':
#         try :
#             WatchList = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist :
#             return Response( {'error': 'WatchList does not exist'}, status = status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(WatchList)
#         return Response(serializer.data)


#     if request.method == 'PUT':
#         WatchList = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(WatchList, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         WatchList = WatchList.objects.get(pk=pk)
#         WatchList.delete()
#         return Response(status =status.HTTP_204_NO_CONTENT)
