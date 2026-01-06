from django.db import models

# Create your models here.




class Category(models.Model):
    name=models.CharField(max_length=80)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name



class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    class Meta:
        ordering=['id',]
        
    def __str__(self):
        return self.name
    

    
from cloudinary.models import CloudinaryField    

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=CloudinaryField('image')
    
    
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator 
   
class Review(models.Model):
    ratings=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Review by {self.user.first_name} on {self.product.name}"
    
    
    
    
    
