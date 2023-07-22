from rest_framework import generics
from .models import Product, Shop, Custom_User, Cart, Category
from .serializers import ProductSerializer, ShopSerializer, Custom_UserSerializer, CustomUserCreateSerializer, CartSerializer, CategorySerializer
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Q, F

# custom user viewset to use custom user serializer
class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserCreateSerializer

#product Views: ProductList, ProductCreate, ProductSearch, ProductDetail, shopProducts
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#this will create a new product only if the user type is shop owner and the user is logged in, the product will be linked automatically to the shop id of the user who is logged in
class ProductCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = AccessToken(token)
        userId = decoded_token['user_id']
        user = Custom_User.objects.get(id=userId)
        serializer.save(shopId=user.shopId)

class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSerializer

    from django.db.models import Q

    def get_queryset(self):
        search = self.request.query_params.get('q', '')
        queryset = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        sort_by = self.request.query_params.get('sort', None)
        filter_by = self.request.query_params.get('filter', None)
        shopId = self.request.query_params.get('shopId', None)
        if sort_by:
            sort_order = self.request.query_params.get('order', 'asc')
            if sort_by == 'price':
                queryset = queryset.order_by(F('price').asc(nulls_last=True) if sort_order == 'asc' else F('price').desc(nulls_last=True))
            elif sort_by == 'date':
                queryset = queryset.order_by(F('created_at').asc(nulls_last=True) if sort_order == 'asc' else F('created_at').desc(nulls_last=True))
        if filter_by:
            filter_by = filter_by.split(',')
            queryset = queryset.filter(categoryId__in=filter_by)
        if shopId:
            queryset = queryset.filter(shopId=shopId)
        return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class shopProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        shopId = self.kwargs['shopId']
        return Product.objects.filter(shopId=shopId)
    

#category Views: CategoryList, CategoryCreate, CategoryDetail

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = AccessToken(token)
        userId = decoded_token['user_id']
        user = Custom_User.objects.get(id=userId)
        serializer.save(shopId=user.shopId)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ShopCategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        shopId = self.kwargs['shopId']
        return Category.objects.filter(shopId=shopId)

#shop Views: ShopList, ShopCreate, ShopDetail
class ShopList(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ShopCreate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = AccessToken(token)
        userId = decoded_token['user_id']
        try:
            user = Custom_User.objects.get(id=userId)
            if user.userType == 'shop_owner':
                serializer = ShopSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(shopOwner=user)
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            return Response({'error': 'Only shop owners can create a shop.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
class ShopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all() 
    serializer_class = ShopSerializer

#user Views: Custom_UserList, Custom_UserDetail
class Custom_UserList(generics.ListAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = Custom_UserSerializer

class Custom_UserDetail(generics.RetrieveAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = Custom_UserSerializer

#cart Views: CartList, CartDetail, UserCartDetail, AddToCart, RemoveFromCart, UpdateCart
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
