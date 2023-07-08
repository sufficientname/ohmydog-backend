from django.urls import include, path
from rest_framework import routers
from ohmydog.advertisements.petsearches import views

router = routers.DefaultRouter()
router.register('petsearches', views.PetSearchAdViewSet, basename='petsearch')

admin_router = routers.DefaultRouter()
admin_router.register('petsearches', views.PetSearchAdAdminViewSet, basename='petsearch')

app_name = 'petsearches_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls)),
]