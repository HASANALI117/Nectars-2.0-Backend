from shop import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('shops/', views.ShopList.as_view()),
    path('shops/<int:pk>/', views.ShopDetail.as_view()),
    path('users/', views.Custom_UserList.as_view()),
    path('users/<int:pk>/', views.Custom_UserDetail.as_view()),
    path('username/', views.username.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)