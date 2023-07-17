from django.contrib import admin
from django.urls import path,include
from web import views
from web . views import PersonApi,PeopleViewset,RegisterApi,LoginApi

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewset, basename='people')
urlpatterns = router.urls
urlpatterns = [
    path('',include(router.urls)),
    path('index',views.index),
    path('person',views.person),
    path('persons',PersonApi.as_view()),
    path('register',RegisterApi.as_view()),
    path('login',LoginApi.as_view())
]
