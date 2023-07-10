from django.urls import include, path
from rest_framework import routers
from ohmydog.campaigns import views

router = routers.DefaultRouter()
router.register('campaigns', views.CampaignViewSet, basename='campaign')

admin_router = routers.DefaultRouter()
admin_router.register('campaigns', views.CampaignAdminViewSet, basename='campaign')

app_name = 'campaigns_app'

urlpatterns = [
    path('users-api/', include(router.urls)),
    path('admin-api/', include(admin_router.urls)),
]