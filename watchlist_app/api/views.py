from attr import fields
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from ..models import Movie



fields = [field.name for field in Movie._meta.get_fields()]    

# fields =["id", "name", "description" ,"active"]


class ApiOverviewAV(APIView):
    def get(self,request):
        api_urls = {
            'List':'http://127.0.0.1:8000/list/',
            'Liste Sorted' : 'http://127.0.0.1:8000/list/?order={field to order by}',
            'Detail View':'http://127.0.0.1:8000/detail/',
            }

        return Response(api_urls)


class MovieListAV(APIView):
    def get(self,request):
        try:
            order = str(request.query_params["order"])   
            if order in fields : 
                 movies = Movie.objects.all().order_by(order)   
            serializer = MovieSerializer(movies, many=True)                         
        except :  
            movies = Movie.objects.all().order_by("id")  #default
            serializer = MovieSerializer(movies, many=True)      
        return Response(serializer.data)                
    def post(self, request):
        serializer = MovieSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors)



 

# @api_view(['GET', 'POST'])
# def movie_list (request):
#     if request.method == 'GET' : 
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST' :
#         serializer = MovieSerializer(data=request.data) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else : 
#             return Response(serializer.errors)                

class MovieDetailsAV (APIView) :
    def get(self,request,pk):
        try : 
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist : 
            return Response( {'error': 'Movie does not exist'}, status = status.HTTP_404_NOT_FOUND)   
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors) 
    def delete(self,request,pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status =status.HTTP_204_NO_CONTENT)



         




# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details (request,pk):
#     if request.method == 'GET':
#         try : 
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist : 
#             return Response( {'error': 'Movie does not exist'}, status = status.HTTP_404_NOT_FOUND)   
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)


#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else : 
#             return Response(serializer.errors)        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status =status.HTTP_204_NO_CONTENT)