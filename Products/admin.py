from django.contrib import admin
from .models import Product, Category, ProductImage, Review
# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('name','description','created_at','updated_at')
    
    
    
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=('product','image')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('product','user','ratings','comment','created_at')
    