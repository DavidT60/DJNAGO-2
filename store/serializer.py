from django.shortcuts import get_list_or_404, get_object_or_404
from django.db import transaction
from decimal import Decimal
from rest_framework import serializers
from . import models 
from . import signals

import base64


# COLLECTION SERIALIZER SECTION #
class CollectionSerializer(serializers.ModelSerializer):
    products_counts = serializers.IntegerField(read_only=True)
    class Meta:
         model = models.Collection
         fields = ['title', 'products_counts']





# REVIEW SERIALIZER SECTION #
class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = models.Review
         fields = ['id','name', 'text']

    def create(self, validated_data):
         get_product_content_id = self.context['product_id']
         return models.Review.objects.create(product_id=get_product_content_id, **validated_data)
    


# product img serializer #
class ProductImgSerializer(serializers.ModelSerializer):
     imgField = serializers.ImageField()
     class Meta:
          model = models.productImg
          fields = ['id','product','imgField']


class ProductPostImgSerializer(serializers.Serializer):
     imgField = serializers.ImageField()
     class Meta:
          model = models.productImg
          fields = ['id','product','imgField']
     
     def create(self, validated_data):
         print("Adding the main request to create")
         get_product_content_id = self.context['product_id']
         print(validated_data)
         print(self.context['request'].FILES)

     #     img_Base64 = self.context['request'].FILES['imgBase'].read()
     #     validated_data['imgBase'] = img_Base64
         return models.productImg.objects.create(product_id=get_product_content_id, **validated_data)
     
     def to_internal_value(self, data):
          print("Testing File Data")
          # print("TO INTERNAL VALUE")
          # print(data)
          # if 'imgBase' in data:
          #      print(self.context['request'].FILES['imgBase'].read())
          #      data['imgBase'] = self.context['request'].FILES['imgBase'].read()
          #      print(data['imgBase'])
          return super().to_internal_value(data)
     
     def validate_imgField(self, value): 
          print("Perform some validatopm for the imageField")
          max_size_kb = 50 * 1024 # kb
          if value.size > max_size_kb:
              raise serializers.ValidationError(f'Image size exceeds maximum limit of {max_size_kb / 1024} kb')
          return value
     
# Product img Serializer #




# PRODUCT SERIALIZER SECTION #
class ProductSerializer(serializers.ModelSerializer): 
 
    def tax_calculation(self, product:models.Product):
             return product.unit_price  
    
    collection = serializers.PrimaryKeyRelatedField(
        queryset= models.Collection.objects.all()
    )
 
    price_with_taxt = serializers.SerializerMethodField(method_name='tax_calculation')
    
    imgs = ProductImgSerializer(many=True, read_only=True)


    class Meta:
        model = models.Product
        fields = ['id','title', 'collection', 'unit_price', 'price_with_taxt', 'imgs']

    #overwritting data:
    def validate(self, attrs):
          print("Data Validation...")
          print(attrs)
          return super().validate(attrs)



# product img serializer #
# class ProductImg(serializers.ModelSerializer):
#      imgBase = serializers.ImageField()
#      class Meta:
#           model = models.productImg
#           fields = ['id','product','imgField']

#      def create(self, validated_data):
#          get_product_content_id = self.context['product_id']
#          img_Base64 = self.context['request'].FILES['imgBase'].read()
#          validated_data['imgBase'] = img_Base64
#          return models.productImg.objects.create(product_id=get_product_content_id, **validated_data)
     
     # def to_internal_value(self, data):
     #      print("TO INTERNAL VALUE")
     #      print(data)
     #      if 'imgBase' in data:
     #           print(self.context['request'].FILES['imgBase'].read())
     #           data['imgBase'] = self.context['request'].FILES['imgBase'].read()
     #           print(data['imgBase'])
     #      return super().to_internal_value(data)


# Cart Items Serializer 
class CartItemsSerializerPatch(serializers.ModelSerializer):
    
    class Meta:
         model = models.CartItem
         fields = [
                   'quantity',
                  ]
 

class CartItemsSerializer(serializers.ModelSerializer):
    
    total_price = serializers.SerializerMethodField()
    product = ProductSerializer()
    
    def get_total_price(self ,model:models.CartItem):
      return model.quantity * model.product.unit_price
    
    class Meta:
         model = models.CartItem
         fields = [
                   'product',
                   'quantity',
                   'total_price',
                  ]
 
    def create(self, validated_data):
         get_cart_content_id = self.context['uui_id']
         print('Unique uuiD')
         print(get_cart_content_id)
         return models.CartItem.objects.create(cart_id=get_cart_content_id, **validated_data)
    

class CartItemsSerializerPost(serializers.ModelSerializer):


     class Meta: 
          model = models.CartItem
          fields = ['id','product', 'quantity']


     # DRF supports a special method naming convention             # 
     # for field-level validation. You can define a method         #
     # named validate_<field_name> within your serializer class.\  #
     # This method receives the serializer instance and the field  #
     # value as arguments.                                         #
     def validate_product_id(self, value):
          if not models.Product.objects.filter(pk=value).exists():
             raise serializers.ValidationError('This Product does not exists.')
          return value
     
     
     def save(self, **kwargs):
          # Current Tranfer:
          cart_id = self.context['uui_id']
          product_id = self.validated_data['product'] 
          quantity = self.validated_data['quantity']
          

          print(cart_id)
          print(product_id)
          print(quantity)
          
          try:
             print("UPDATE")
             update_cartitmes = models.CartItem.objects.get(cart_id=cart_id, product_id=product_id)
             update_cartitmes.quantity += quantity
             update_cartitmes.save()
             self.instance = update_cartitmes
          except models.CartItem.DoesNotExist:        
             print("CREATE")
             create_cartitmes = models.CartItem.objects.create(cart_id=cart_id, **self.validated_data)
             create_cartitmes.save()
             self.instance = create_cartitmes
            
          return self.instance

# Order Serializer #
class OrderItemsSerializer(serializers.ModelSerializer):
      class Meta:
           model=models.OrderItem
           fields = ['product', 'quantity', 'unit_price']




class CustomerSerializer(serializers.ModelSerializer):    
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
         model = models.Customer
         fields = [
          'user_id',
          'phone',
          'birth_date',
          'membership'
         ]

class OrderSerializer(serializers.ModelSerializer):
     id = serializers.IntegerField(read_only=True)
     customer = CustomerSerializer(read_only=True)
     items = OrderItemsSerializer(many=True, read_only=True)

     class Meta:
          model = models.Order
          fields = ['id','placed_at','payment_status','customer','items']

class OrderCreateSerializer(serializers.Serializer):
     cart_id = serializers.UUIDField()

     # Called before calls the sace methos #
     def validate_cart_id(self, cart_id):
          if not models.Cart.objects.filter(pk=cart_id).exists():
               raise serializers.ValidationError(f'the cart id {cart_id} does not exist')
          if models.CartItem.objects.filter(cart_id=cart_id).count()==0:
               raise serializers.ValidationError(f'the items in this cart are Empty')
          
          return cart_id
     
     def save(self, **kwargs):
        with transaction.atomic():
          print("Running Transaction Proccess....")

          cart_id = self.validated_data['cart_id'] # Get the cart id
          get_user_id = self.context['get_user_id'] # get the user id form customer 
          print(cart_id)
          print(get_user_id)
          # Getting Customer from User id  #
          (customer, created) = models.Customer.objects.get_or_create(user_id=get_user_id)
     
          # Create Order Table #
          order_customer_created = models.Order.objects.create(customer=customer)

          # filter the cartitems table #
          cartItems = models.CartItem.objects.select_related('product').filter(cart_id=cart_id)
      
          # Create OrdenItems Table # 
          order_items = [models.OrderItem(
               order=order_customer_created,
               product=cartItems.product,
               quantity=cartItems.quantity,
               unit_price=cartItems.product.unit_price
          ) for cartItems in cartItems]

          models.OrderItem.objects.bulk_create(order_items)
         
          # Delete Cart Row #
          print("Deleting Cart...")
          models.Cart.objects.filter(pk=cart_id).delete()

          # IT created a order send to Trigger Signal #
          signals.customer_order_created.send_robust(self.__class__, order=order_customer_created)
         
          return order_customer_created
          

# Cart Serializer 
class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    cartitems = CartItemsSerializer(many=True, read_only=True)    
    total_to_pay = serializers.SerializerMethodField()

    def get_total_to_pay(self, cart):
         total = sum([items.quantity * items.product.unit_price for items in cart.cartitems.all()])
         return total
    
    class Meta:
         model = models.Cart
         fields = [
              'id',
              'created_at',
              'cartitems',
              'total_to_pay',
         ]



# cart Itmes
# In the time saving the data Update Quantity
# Product:     quantity:      total_to_play:  
#  Mango          3              30$

#> When add another mango to the table it will no add a new roll like: 

# In the time saving the data Update Quantity
# Product:     quantity:      total_to_play:  
#  Mango          3              30$
#  Mango          2              20$

# Insted the idea is the next:
# In the time saving the data Update Quantity
# Product:     quantity:      total_to_play:  
#  Mango          5              50$
