from rest_framework import serializers
from . models import Person,Color

from django.contrib.auth.models import User
class ColorSerializer (serializers.ModelSerializer):
    class Meta:
        model=Color
        fields=["color_name"]

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    #Create a field without model
    country = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields='__all__'
        #depth=1 - it shows all fields, but only need colorname so we create a serializer for color
       
    def validate(self,data):
        special_char = "!@#$%^&*()_"
        if data['age']<18:
            raise serializers.ValidationError("Age should greater than 18")
       
        if any(c in special_char for c in data['name']):
            raise serializers.ValidationError("Name should be alphabet")
        
        return data
    
    #Fix assertion error
    def create(self, validate):
            color = validate.pop('color')
            instance = Person.objects.create(**validate)
            instance.Color = color
            return instance

        
    def update(self, data, validate):
       
        instance = Person.objects.create(**validate)
      
        instance.save()
        return validate
    #     return validate
    def get_country(self,objs):
        return "india "


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    # check a user or not
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exist")
        if data['email']:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("email already exist")
        return data
    
    def create(self, validated_data):
        user=User.objects.create_user(username=validated_data['username'],email=validated_data["email"],password=validated_data['password'])
        
        user.save()
        return validated_data 
       
class LoginSerialzer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
