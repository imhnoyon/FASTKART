from django.db import models
from Users.models import User
from Products.models import Product
from uuid import uuid4


class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart {self.id} by {self.user.first_name}"
    
    
    
    
class CartItem(models.Model):
    quantity=models.PositiveIntegerField()
    
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    class Meta:
        unique_together=['cart','product']
        
        
    def __str__(self):
        return f"{self.quantity} X {self.product.name}"
    
    
    
class Order(models.Model):
    NOT_PAID = 'Not Paid'
    READY_TO_SHIP='Ready To Ship'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (NOT_PAID, 'Not Paid'),
        (READY_TO_SHIP, 'Ready To Ship'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=NOT_PAID)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    
    def __str__(self):
        return f"Order {self.id} by {self.user.first_name} -> {self.status}"
    
    
class OrderItem(models.Model):
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    total_price =models.DecimalField(max_digits=12,decimal_places=2)
    
    
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name} in Order {self.order.id}"
    
     
    
    