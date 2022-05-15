from attr import fields
from rest_framework import serializers
from validator import Validator
from ..models import WatchList, StreamPlatform, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = "__all__"
        exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        #depth = 1


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        # exclude = ['id']
        fields = '__all__'
        #depth = 1

    # id= serializers.IntegerField(read_only= True)
    # name= serializers.CharField(max_length=40, validators=[name_length])
    # description= serializers.CharField(max_length = 200)
    # active= serializers.BooleanField(validators = [is_active])

    # def create(self,validated_data):
    #     return WatchList.objects.create(**validated_data)

    # def update(self,instance,validated_data):
    #     instance.name = validated_data.get('name', instance.name) #instance.name is the old name
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active',instance.active)
    #     instance.save()
    #     return instance
