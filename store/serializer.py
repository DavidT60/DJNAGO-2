from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review


# COLLECTION SERIALIZER SECTION #
class CollectionSerializer(serializers.ModelSerializer):
    products_counts = serializers.IntegerField(read_only=True)
    class Meta:
         model = Collection
         fields = ['title', 'products_counts']


# PRODUCT SERIALIZER SECTION #
class ProductSerializer(serializers.ModelSerializer): 
 
    def tax_calculation(self, product:Product):
             return product.unit_price  
    
    collection = serializers.PrimaryKeyRelatedField(
        queryset= Collection.objects.all()
    )
 
    price_with_taxt = serializers.SerializerMethodField(method_name='tax_calculation')


    class Meta:
        model = Product
        fields = ['title', 'collection', 'unit_price', 'price_with_taxt']

    # overwritting data:
    def validate(self, attrs):
          print("Data Validation...")
          print(attrs)
          return super().validate(attrs)

# COLLECTION SERIALIZER SECTION #
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
         model = Review
         fields = ['id','name', 'text']
    
    def create(self, validated_data):
         get_product_content_id = self.context['product_id']
         return Review.objects.create(product_id=get_product_content_id, **validated_data)