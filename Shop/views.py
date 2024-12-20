from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Project import settings
from .models import Product, Review, Cart, Order, Category, Wishlist
from .serializers import ProductSerializer, ReviewSerializer, CartSerializer, OrderSerializer, CategorySerializer, \
    WishlistSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs['product_id'])
        serializer.save(product=product, user=self.request.user)


# Cart ViewSet
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_cart = Cart.objects.filter(user=self.request.user)
        total_price = sum(item.product.price * item.quantity for item in user_cart)
        serializer.save(user=self.request.user, total_price=total_price)


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Wishlist ViewSet
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# JWT Login and Registration Views

# Advanced Search View
class AdvancedSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        products = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
