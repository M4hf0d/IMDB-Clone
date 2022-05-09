from black import validate_metadata
from rest_framework import serializers
from ..models import Movie


class MovieSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only= True)
    name= serializers.CharField(max_length=40)
    description= serializers.CharField(max_length = 200)
    active= serializers.BooleanField()
    def create(self,validated_data):
        return Movie.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name', instance.name) #instance.name is the old name 
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active',instance.active)
        instance.save()
        return instance
