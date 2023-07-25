from rest_framework import serializers
from .models import Product, Shop, Custom_User, Cart, Category, ShopProps

from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Custom_User
        fields = ("id", "username", "email", "password", "userType", "shopId")


class ShopSerializer(serializers.ModelSerializer):
    shopOwner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Shop
        fields = ["shopId", "shopName", "description", "shopOwner"]


class ShopPropsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProps
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    shopId = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    shopId = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ["categoryId", "name", "description", "shopId"]


class Custom_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
