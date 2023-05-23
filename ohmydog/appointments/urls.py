from django.urls import include, path
from rest_framework import routers
from ohmydog.appointments import views

router = routers.DefaultRouter()
router.register('appointments', views.AppointmentViewSet, basename='appointment')

admin_router = routers.DefaultRouter()
admin_router.register('appointments', views.AppointmentAdminViewSet, basename='appointment')

app_name = 'appointments_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls)),
]