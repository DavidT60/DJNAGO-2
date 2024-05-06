from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.aggregates import Count
from django import forms

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import django_filters


from .models import Product, Collection, Review
from .serializer import ProductSerializer, CollectionSerializer, ReviewSerializer


# COLLECTION VIEW SECTION #
class CollectionModelView(ModelViewSet):
    """DOCUMENTATION ABOUT THIS MODULE"""
    queryset = Collection.objects.all().annotate(products_counts=Count('product')) 

   
    def get_serializer_class(self):
       return CollectionSerializer
    
    def get_serializer_context(self):
       return {'request': self.request}    

    def destroy(self, request, *args, **kwargs):
       collection_object =  Collection.objects.all().filter(pk=kwargs['pk']).annotate(products_counts=Count('product'))
       collection_records_returned = len(list(collection_object))
       if collection_records_returned <= 0:
             return Response({'error':'This collection Does not exits'}, status=status.HTTP_404_NOT_FOUND)
       collection_product_count = collection_object[0].products_counts
       if collection_product_count > 0:
             return Response({'error':f'This Collection Can not be delete, There are {collection_product_count} ordered items with this collection'}, status=status.HTTP_501_NOT_IMPLEMENTED)
       return super().destroy(request, *args, **kwargs)



class ProductFilter(filters.FilterSet):

    unit_price = django_filters.LookupChoiceFilter(
            field_class=forms.DecimalField,
            lookup_choices=[
                ('exact', 'Equals'),
                ('gt', 'Greater than'),
                ('lt', 'Less than'),
            ]
        )
 
    min_date = filters.DateRangeFilter(field_name="last_update")
 
 
    class Meta:
        model = Product
        fields = ['collection']


class ProductModelView(ModelViewSet):
   """Product Class View"""
   filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   filterset_class = ProductFilter
   search_fields = ['title']
   ordering_fields = [
       'last_update'
   ]

   def get_queryset(self):
      req= self.request
      queryset =  Product.objects.select_related('collection').all()

      # URL BODY: http://127.0.0.1:8000/store/product/?collection_id=3
      collection_id = req.query_params.get('collection_id')
      if collection_id != None:
          return queryset.filter(collection_id=collection_id)  
      return queryset
        

   def get_serializer_class(self, *args, **kwargs):
      return ProductSerializer
   
   def get_serializer_context(self):
      return {'request': self.request}
 

   def destroy(self, request, *args, **kwargs):
       product_object = get_object_or_404(Product, pk=kwargs['pk'])
       orderItem_product_count = product_object.orderitems.count()
       print(orderItem_product_count)
       if orderItem_product_count > 0:
             return Response({'error':f'This Product Can not be delete, There are {orderItem_product_count} items ordered'})
       return super().destroy(request, *args, **kwargs)
   

   

# REVIEW VIEW SECTION #
class ReviewModelVIew(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
     
    def get_serializer_class(self):
       return ReviewSerializer
    
    def get_serializer_context(self):
       return {
          'product_id': self.kwargs['product_pk']
       }