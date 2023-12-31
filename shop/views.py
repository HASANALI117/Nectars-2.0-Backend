from rest_framework import generics
from .models import Product, Shop, Custom_User, Cart
from .serializers import ProductSerializer, ShopSerializer, Custom_UserSerializer, CustomUserCreateSerializer, CartSerializer
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

class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDetail(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# this will return the cart details of the user who is logged in
class UserCartDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_object(self):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            decoded_token = AccessToken(token)
            userId = decoded_token['user_id']
            user = Custom_User.objects.get(id=userId)
            cart = Cart.objects.get(userId=user)
            return cart
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            decoded_token = AccessToken(token)
            userId = decoded_token['user_id']
            user = Custom_User.objects.get(id=userId)
            cart = Cart.objects.get(userId=user)
            product = Product.objects.get(productId=request.data['productId'])
            product_serializer = ProductSerializer(product)
            product_data = product_serializer.data
            # Check if product is already in cart
            for item in cart.products:
                if item['productId'] == product_data['productId']:
                    item['quantity'] += 1
                    cart.save()
                    return Response({'success': 'Product quantity updated successfully.'}, status=200)
            # If product is not in cart, add it with quantity 1
            product_data['quantity'] = 1
            cart.products.append(product_data)
            cart.save()
            return Response({'success': 'Product added to cart successfully.'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
class RemoveFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            decoded_token = AccessToken(token)
            userId = decoded_token['user_id']
            user = Custom_User.objects.get(id=userId)
            cart = Cart.objects.get(userId=user)
            
            # Check if product is in cart
            for item in cart.products:
                print(item)
                if item['productId'] == request.data['productId']:
                    cart.products.remove(item)
                    cart.save()
                    return Response({'success': 'Product removed from cart successfully.'}, status=200)
            # If product is not in cart, return error
            return Response({'error': 'Product not found in cart.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class UpdateCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            decoded_token = AccessToken(token)
            userId = decoded_token['user_id']
            user = Custom_User.objects.get(id=userId)
            cart = Cart.objects.get(userId=user)
            
            # Check if product is in cart
            for item in cart.products:
                if item['productId'] == request.data['productId']:
                    item['quantity'] = request.data['quantity']
                    cart.save()
                    return Response({'success': 'Product quantity updated successfully.'}, status=200)
            # If product is not in cart, return error
            return Response({'error': 'Product not found in cart.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

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
