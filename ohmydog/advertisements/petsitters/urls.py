from django.urls import include, path
from rest_framework import routers
from ohmydog.advertisements.petsitters import views

router = routers.DefaultRouter()
router.register('petsitters', views.PetSitterAdViewSet, basename='petsitter')

admin_router = routers.DefaultRouter()
admin_router.register('petsitters', views.PetSitterAdAdminViewSet, basename='petsitter')

app_name = 'petsitters_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls)),
]