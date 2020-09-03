from django.urls import path, include
from rest_framework import routers
# from rest_framework.routers import DefaultRouter
from Business.views import BusinessViewSet

router = routers.DefaultRouter()
router.register('business', BusinessViewSet, basename='business')

app_name = 'Business'

urlpatterns = [
    path('update/', BusinessViewSet.as_view({"put": "update"})),
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
