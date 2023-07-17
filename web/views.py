from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import  Person
from . serializer import PeopleSerializer,ColorSerializer,RegisterSerializer,LoginSerialzer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# Create your views here.
@api_view(['GET','POST'])
def index(request):
    course={
        'name':'python',
        'learn':"['flask','django']"
    }
    # if request.method=="GET":
    #     print("GET")
    #     return Response(course)
    # elif request.method=="POST":
    #     print("POST")
    #     return Response(course)
    # return Response(course)

    if request.method=="GET":
        print("GET")
        return Response(course)
    elif request.method=="POST":
        #Front end to back
        data = request.data
        print(data)
        return Response(data)
    return Response(course)
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method=="GET":
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        data = request.data
        serializer=PeopleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=="PUT":
        data = request.data
        objs = Person.objects.get(id=data['id']) 
        serializer=PeopleSerializer(objs, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=="PATCH":
        
        data = request.data
        objs = Person.objects.get(id=data['id']) 
        serializer=PeopleSerializer(objs,data=data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
       
        data = request.data
        objs=Person.objects.get(id=data['id'])
        objs.delete()
        return Response({'message':'person deleted'})
        


### Now we test apiview instead of apiview decorator

class PersonApi(APIView):
    def get(self,request):
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        serializer=PeopleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def put(self,request):
        data = request.data
        objs = Person.objects.get(id=data['id']) 
        serializer=PeopleSerializer(objs, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self,request):
        
        data = request.data
        objs = Person.objects.get(id=data['id']) 
        serializer=PeopleSerializer(objs,data=data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request):
       
        data = request.data
        objs=Person.objects.get(id=data['id'])
        objs.delete()
        return Response({'message':'person deleted'})
        
### We write so many codes for crud,but if we use model viewset, its quite simple

## import necessary documents

class PeopleViewset(viewsets.ModelViewSet):
    serializer_class=PeopleSerializer
    queryset=Person.objects.all()

#search function
    def list(self,request):
        search = request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer = PeopleSerializer(queryset,many=True)
        return Response({
                "status":200,'data':serializer.data
            })

class RegisterApi(APIView):
    def post(self,request):
        data = request.data 
        serializer=RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({'status':False,'message':serializer.errors})
        serializer.save()
        return Response({'status':True,'message':"User Created"},status.HTTP_201_CREATED)
    
class LoginApi(APIView):
    def post(self,request):
        data = request.data 
        serializer=LoginSerialzer(data=data)
        
        if not serializer.is_valid():
            return Response({'status':False,'message':serializer.errors})
        
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        return Response({'status':True,'message':"User Created"},status.HTTP_201_CREATED)
    
