from django.urls import include, path
from rest_framework import routers
from ohmydog.users import views
from rest_framework.authtoken.views import ObtainAuthToken


admin_router = routers.DefaultRouter()
admin_router.register('users', views.AdminUserViewSet, basename='user')

app_name = 'users_app'

urlpatterns = [
    path('users-api/users/me/', views.UserMeApiView.as_view(), name='user-me'),
    path('users-api/users/me/password/', views.UserMePasswordApiView.as_view(), name='user-me-password'),
    path('admin-api/', include(admin_router.urls)),
]