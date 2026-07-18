from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "inventory_api"
router = DefaultRouter()
# Daftarkan ViewSet Anda di sini
# router.register(r'items', views.ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
