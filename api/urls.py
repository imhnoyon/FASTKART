from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Products.views import ProductViewSet, CategoryViewSet, ProductImageViewSet, ReviewViewSet
router=DefaultRouter()

router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet,basename='categories')
router.register('product-images',ProductImageViewSet,basename='product-images')
router.register('reviews',ReviewViewSet,basename='reviews')

urlpatterns = [
    path('auth/', include('djoser.urls')),    
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/',include(router.urls)),  
]




