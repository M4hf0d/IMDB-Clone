from rest_framework import serializers
from validator import Validator
from ..models import Movie


def name_length(value) :
    if len(value) < 2 :
        raise serializers.ValidationError("name is too short")
    return value
def is_active(value) :
    if value is False :
        raise serializers.ValidationError("inactive movie can't be added to database")
    return value    


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    def validate_name(self, value): #field validation
      
        if len(value) < 2 :
            raise serializers.ValidationError("name is too short")
        return value

    def validate(self, data): #objects level validation
    
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and description should be the different")
        return data    


    # id= serializers.IntegerField(read_only= True)
    # name= serializers.CharField(max_length=40, validators=[name_length])
    # description= serializers.CharField(max_length = 200)
    # active= serializers.BooleanField(validators = [is_active])


    # def create(self,validated_data):
    #     return Movie.objects.create(**validated_data)


    # def update(self,instance,validated_data):
    #     instance.name = validated_data.get('name', instance.name) #instance.name is the old name 
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active',instance.active)
    #     instance.save()
    #     return instance