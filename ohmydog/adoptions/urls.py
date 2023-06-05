from django.urls import include, path
from rest_framework import routers
from ohmydog.adoptions import views

router = routers.DefaultRouter()
router.register('adoptions', views.AdoptionAdViewSet, basename='adoption')

app_name = 'adoptions_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
]