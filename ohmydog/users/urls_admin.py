from django.urls import include, path
from rest_framework import routers
from ohmydog.users import views


admin_router = routers.DefaultRouter()
admin_router.register('users', views.AdminUserViewSet, basename='user')

app_name = 'users_app'

urlpatterns = [
    path('admin-api/', include(admin_router.urls)),
]