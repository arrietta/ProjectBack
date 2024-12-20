from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_swagger_view
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ReviewViewSet, CartViewSet, OrderViewSet, CategoryViewSet, WishlistViewSet, AdvancedSearchView

schema_view = get_swagger_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for my DRF project",
    ),
    public=True,

)
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'cart', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'wishlist', WishlistViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('search/', AdvancedSearchView.as_view(), name='search'),


]
