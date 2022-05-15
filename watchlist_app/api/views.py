from platform import platform
from attr import fields
from watchlist_app.models import WatchList
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from ..models import WatchList,StreamPlatform



fields = [field.name for field in WatchList._meta.get_fields()]    

# fields =["id", "name", "description" ,"active"]


class ApiOverviewAV(APIView):
    def get(self,request):
        api_urls = {
            'List':'http://127.0.0.1:8000/list/',
            'Liste Sorted' : 'http://127.0.0.1:8000/list/?order={field to order by}',
            'Detail View':'http://127.0.0.1:8000/detail/',
            }
        return Response(api_urls)


class WatchListAV(APIView):
    def get(self,request):
        try:
            order = str(request.query_params["orderby"])   
            if order in fields : 
                 Movies = WatchList.objects.all().order_by(order)   
            serializer = WatchListSerializer(Movies, many=True)                         
        except :  
            Movie = WatchList.objects.all().order_by("id")  #default
            serializer = WatchListSerializer(Movie, many=True)      
        return Response(serializer.data)                
    def post(self, request):
        serializer = WatchListSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors)




class WatchListDetailsAV (APIView) :
    def get(self,request,pk):
        try : 
            Movies = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist : 
            return Response( {'error': 'WatchList does not exist'}, status = status.HTTP_404_NOT_FOUND)   
        serializer = WatchListSerializer(Movies)
        return Response(serializer.data)

    def put(self,request,pk):
        Movies = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(Movies, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors) 
    def delete(self,request,pk):
        Movies = WatchList.objects.get(pk=pk)
        Movies.delete()
        return Response(status =status.HTTP_204_NO_CONTENT)



class StreamPlatformAV(APIView):
    def get(self,request): 
        Platforms = StreamPlatform.objects.all()  #default
        serializer = StreamPlatformSerializer(Platforms, many=True)      
        return Response(serializer.data)                
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors)


class StreamPlatformDetailsAV(APIView) :
    def get(self,request,pk):
        try : 
            platforms = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist : 
            return Response( {'error': 'Platform does not exist'}, status = status.HTTP_404_NOT_FOUND)   
        serializer = StreamPlatformSerializer(platforms)
        return Response(serializer.data)

    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors) 
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status =status.HTTP_204_NO_CONTENT)


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