from django.urls import path
from .views import HomeView,ProductDetailView,ShopView,search_shop


app_name='product'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-detail/<str:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/<str:slug>/', search_shop, name='shop-search'),
  
]
