"""
URL configuration for ohmydog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('ohmydog.users.urls', namespace='users')),

    path('', include('ohmydog.pets.urls', namespace='pets')),
    path('', include('ohmydog.appointments.urls', namespace='appointments')),
    path('', include('ohmydog.advertisements.adoptions.urls', namespace='adoptions')),
    path('', include('ohmydog.advertisements.petsearches.urls', namespace='petsearches')),
    path('', include('ohmydog.advertisements.petsitters.urls', namespace='petsitters')),
]
