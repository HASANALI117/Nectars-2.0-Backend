from rest_framework import serializers
from .models import Product, Shop, Custom_User, Cart

from djoser.serializers import UserCreateSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Custom_User
        fields = ('id', 'username', 'email', 'password', 'userType', 'shopId')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['shopId', 'shopName', 'description', 'shopOwner']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'name', 'description', 'price', 'shopId', 'created_at', 'updated_at']

class Custom_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'