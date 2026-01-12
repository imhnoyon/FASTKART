from rest_framework import serializers
from .models import Order,OrderItem,Cart,CartItem
from Products.models import Product
from Products.serializers import ProductSerializer


# ১. খালি সিরিয়ালাইজার: অনেক সময় কোনো ইনপুট ছাড়াই অ্যাকশন পারফর্ম করতে এটি লাগে।
class EmptySerializer(serializers.Serializer):
    pass





# ২. ছোট প্রোডাক্ট সিরিয়ালাইজার: কার্ট বা অর্ডারের ভেতরে প্রোডাক্টের শুধু আইডি, নাম আর দাম দেখানোর জন্য।
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        
        
        
        
 # ৩. কার্টে আইটেম যোগ করার সিরিয়ালাইজার: ইউজার যখন কোনো প্রোডাক্ট কার্টে ঢোকাতে চায়।       
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
        
        
    # প্রোডাক্ট আইডি চেক করা: ডাটাবেসে এই আইডি আছে কি না তা যাচাই করে।
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exists")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            # যদি আইটেমটি আগে থেকেই কার্টে থাকে, তবে শুধু কোয়ান্টিটি বাড়িয়ে দাও
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # না থাকলে নতুন করে তৈরি করো
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    
    
    
# ৪. আইটেম আপডেট সিরিয়ালাইজার: কার্টে থাকা কোনো জিনিসের পরিমাণ (quantity) কমানো বা বাড়ানোর জন্য।    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
        
# ৫. কার্ট আইটেম লিস্ট সিরিয়ালাইজার: কার্টের ভেতরে প্রতিটি আইটেমকে সুন্দরভাবে সাজিয়ে দেখানোর জন্য।        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() 
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    # আইটেমের মোট দাম ক্যালকুলেট করছে
    def get_total_price(self, cart_item: CartItem):
        
        return cart_item.quantity * cart_item.product.price
    
    
# ৬. মেইন কার্ট সিরিয়ালাইজার: পুরো কার্টের তথ্য এবং সব আইটেম মিলিয়ে সর্বমোট বিল দেখানোর জন্য।    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        # return sum([item.product.price * item.quantity for item in cart.items.all()])
        total_price = 0
        for item in cart.items.all():
            sum = item.product.price * item.quantity
            total_price = total_price + sum

        return total_price
    
    
 
# ৭. অর্ডার আইটেম সিরিয়ালাইজার: অর্ডার হয়ে যাওয়ার পর মেমোতে প্রতিটি আইটেমের ডিটেইলস দেখানোর জন্য।
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity', 'total_price']
 
 
 
 
 
# ৮. অর্ডার তৈরি করার সিরিয়ালাইজার: কার্ট থেকে ডেটা নিয়ে ফাইনাল অর্ডার প্লেস করার জন্য।    
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        # কার্ট আইডি সঠিক কি না এবং কার্টটি খালি কি না চেক করছে
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']
        try:
            # সার্ভিস ফাইল থেকে অর্ডার তৈরির মেইন লজিক কল করছে
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        # অর্ডার তৈরি হওয়ার পর ডাটাগুলো OrderSerializer ফরম্যাটে দেখাবে
        return OrderItemSerializer(instance).data
    
    
    
    
    
    
# ৯. অর্ডার আপডেট সিরিয়ালাইজার: অর্ডারের স্ট্যাটাস (যেমন: Pending থেকে Shipped) পরিবর্তন করার জন্য।   
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        
        


# ১০. ফাইনাল অর্ডার সিরিয়ালাইজার: ইউজারের কাছে অর্ডারের পূর্ণাঙ্গ রিসিট বা ডিটেইলস দেখানোর জন্য।       
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']