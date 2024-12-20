from rest_framework import serializers
from .models import Product, Review, Cart, Order, Category, Wishlist
from django.contrib.auth.models import User

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'category']

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'content', 'created_at']

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    products = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'products', 'total_price', 'shipping_address', 'status', 'created_at']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']

# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Wishlist
        fields = ['id', 'product']
