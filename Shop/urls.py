from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ReviewViewSet, CartViewSet, OrderViewSet, CategoryViewSet, WishlistViewSet, AdvancedSearchView

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
