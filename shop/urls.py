from shop import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/create/', views.ProductCreate.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/search/', views.ProductSearch.as_view()),
    path('shopProducts/<int:shopId>/', views.shopProducts.as_view()),
    path('shops/', views.ShopList.as_view()),
    path('shops/create/', views.ShopCreate.as_view()),
    path('shops/<int:pk>/', views.ShopDetail.as_view()),
    path('shops/<str:shopName>/', views.ShopDetailFromName.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/create/', views.CategoryCreate.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('categories/shop/<int:shopId>/', views.ShopCategoryList.as_view()),
    path('users/', views.Custom_UserList.as_view()),
    path('users/<int:pk>/', views.Custom_UserDetail.as_view()),
    path('username/', views.username.as_view()),
    path('carts/', views.CartList.as_view()),
    path('carts/<int:pk>/', views.CartDetail.as_view()),
    path('userCart/', views.UserCartDetail.as_view()),
    path('addToCart/', views.AddToCart.as_view()),
    path('removeFromCart/', views.RemoveFromCart.as_view()),
    path('updateCart/', views.UpdateCart.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)