from rest_framework import serializers
from .models import Product, Shop, Custom_User, Cart, Category

from djoser.serializers import UserCreateSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Custom_User
        fields = ('id', 'username', 'email', 'password', 'userType', 'shopId')


class ShopSerializer(serializers.ModelSerializer):
    shopOwner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Shop
        fields = ['shopId', 'shopName', 'description', 'shopOwner']

class ProductSerializer(serializers.ModelSerializer):
    shopId = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['productId', 'name', 'description', 'price', 'shopId', 'categoryId', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    shopId = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = ['categoryId', 'name', 'description', 'shopId']

class Custom_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'