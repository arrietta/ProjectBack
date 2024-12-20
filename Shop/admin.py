from django.contrib import admin
from .models import Product, Category, Review, Cart, Order, Wishlist

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
