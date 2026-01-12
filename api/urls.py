from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Products.views import ProductViewSet, CategoryViewSet, ProductImageViewSet, ReviewViewSet
from orders.views import OrderViewset,CartViewSet,CartItemViewSet
from rest_framework_nested import routers

router=DefaultRouter()

router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet,basename='categories')
router.register('product-images',ProductImageViewSet,basename='product-images')
router.register('reviews',ReviewViewSet,basename='reviews')



router.register('carts',CartViewSet, basename='carts')
router.register('orders',OrderViewset,basename='orders')
router.register('cart-items',CartItemViewSet, basename='cart-items')

product_router = routers.NestedDefaultRouter( router, 'products', lookup='product')
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')

urlpatterns = [
    path('auth/', include('djoser.urls')),    
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/',include(router.urls)),  
]




