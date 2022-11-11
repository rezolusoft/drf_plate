from rest_framework.routers import DefaultRouter
from core.auth.viewsets import (register, login, logout)

from django.urls import path, include

Router = DefaultRouter(trailing_slash=False)

# Authentication
Router.register('register', register.RegisterViewSet, basename='auth')
Router.register('login', login.ObtainAuthToken, basename='auth-login')
Router.register('logout', logout.LogoutViewSet, basename='auth-logout')



urlpatterns = [

    path('', include(Router.urls))

]
