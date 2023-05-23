from django.urls import include, path
from rest_framework import routers
from ohmydog.pets import views

router = routers.DefaultRouter()
router.register('pets', views.PetViewSet, basename='pet')

admin_router = routers.DefaultRouter()
admin_router.register('pets', views.PetAdminViewSet, basename='pet')

app_name = 'pets_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls))
]