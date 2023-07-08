from django.urls import include, path
from rest_framework import routers
from ohmydog.advertisements.adoptions import views

router = routers.DefaultRouter()
router.register('adoptions', views.AdoptionAdViewSet, basename='adoption')

admin_router = routers.DefaultRouter()
admin_router.register('adoptions', views.AdoptionAdAdminViewSet, basename='adoption')

app_name = 'adoptions_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls)),
]