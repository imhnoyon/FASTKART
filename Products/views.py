from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Product,ProductImage,Category,Review
from .serializers import ProductSerializer,ImageSerializer,CategorySerializers,ReviewSerializer
from .permissions import IsAdminOrReadOnly,IsReviewAuthorOrReadonly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import FilterSet
from .pagination import DefaultPagination



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    FilterSet_class = FilterSet
    search_fields = ['name','description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]
    
    
    # ১. ডেটা কোয়েরি করার সময় ছবিগুলোসহ নিয়ে আসা (Optimization)
    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    # ২. ডিলিট করার সময় নিজস্ব একটি শর্ত যোগ করা
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        
        # যদি স্টক ১০ এর বেশি হয়, ডিলিট করতে দিবে না
        if product.stock > 10:
            return Response(
                {'error': "বেশি স্টক থাকা প্রোডাক্ট ডিলিট করা যাবে না।"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    # helper function - যা কোড রিপিটেশন কমাবে
    def get_product_id(self):
        return self.kwargs.get('product_pk')

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.get_product_id())

    def perform_create(self, serializer):
        serializer.save(product_id=self.get_product_id())
        
        
        
from django.db.models import Count        
class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.annotate(product_count=Count('products',distinct=True)).all()
    serializer_class=CategorySerializers
    
    
    
    
class ReviewViewSet(ModelViewSet):
    #eikhane queryset na diye get_queryset method use kora better karon ami sob product er review dekhbo na ,je product er review dorkar seita dekhbo
    serializer_class= ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadonly]
    
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
    
    