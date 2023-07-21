from rest_framework import generics
from .models import Product, Shop, Custom_User
from .serializers import ProductSerializer, ShopSerializer, Custom_UserSerializer, CustomUserCreateSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserCreateSerializer
     
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ShopList(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ShopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all() 
    serializer_class = ShopSerializer

class Custom_UserList(generics.ListAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = Custom_UserSerializer

class Custom_UserDetail(generics.RetrieveAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = Custom_UserSerializer

class username(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        print(token)
        try:
            decoded_token = AccessToken(token)
            userId = decoded_token['user_id']
            user = Custom_User.objects.get(id=userId)
            username = user.username
            # print(decoded_token['user_id'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        content = {'message': f'Hello, {username}!'}
        return Response(content)
