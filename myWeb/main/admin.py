from django.contrib import admin
from .models import Category, Product, Cart, CartDetail,Review,Checkout

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartDetail)
admin.site.register(Review)
admin.site.register(Checkout)