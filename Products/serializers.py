from rest_framework import serializers
from .models import Category,Product,Review,ProductImage
from decimal import Decimal


class CategorySerializers(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True, help_text='Return the number product in this category')
    class Meta:
        model=Category
        fields=['id','name','description','product_count']
        
    



class ImageSerializer(serializers.ModelSerializer):
    # image=serializers.ImageField()
    class Meta:
        model = ProductImage
        fields=['id','image']
        


class ProductSerializer(serializers.ModelSerializer):
    images=ImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=['id','name','description','price','stock','category','price_with_tax','images']
        
        
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')   
    
    def calculate_tax(self,product):
        return round(product.price + (product.price * Decimal(0.1)),2)         
    
    def validate_price(self,price):
        if price < 0:
            raise serializers.ValidationError('price could not be negative')
        return price
    
    


from django.contrib.auth import get_user_model

# class SimpleUserSerializer(serializers.ModelSerializer):
#     # SerializerMethodField এর বদলে সরাসরি 'get_full_name' সোর্স ব্যবহার করা যায়
#     name = serializers.CharField(source='get_full_name', read_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'name']
 
    
# class ReviewSerializer(serializers.ModelSerializer):
#     user = SimpleUserSerializer(read_only=True)
#     class Meta:
#         model=Review
#         fields=['id','product','user','ratings','comment','updated_at']
#         read_only_fields=['product','user']
        
 
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model=Review
        fields=['id','product','user','ratings','comment','updated_at']
        read_only_fields=['product','user']   
            
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)