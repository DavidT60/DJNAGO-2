from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.aggregates import Count
from django import forms


from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import django_filters
import base64



from . import permissions as permisionCustom
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, productImg
from . import serializer as Serializer

# COLLECTION VIEW SECTION #
class CollectionModelView(ModelViewSet):
    """DOCUMENTATION ABOUT THIS MODULE"""
    queryset = Collection.objects.all().annotate(products_counts=Count('product')) 
    permission_classes = [permisionCustom.DjanggoObjectsPermisions]
   
    def get_serializer_class(self):
       return Serializer.CollectionSerializer
    
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
#    permission_classes = [permisionCustom.DjanggoObjectsPermisions]
   ordering_fields = [
       'last_update'
   ]

   def get_queryset(self):
      req= self.request
      queryset =  Product.objects.select_related('collection').prefetch_related('imgs').all()

      # URL BODY: http://127.0.0.1:8000/store/product/?collection_id=3http://127.0.0.1:8000/store/product/?collection_id=3
      collection_id = req.query_params.get('collection_id')
      if collection_id != None:
          return queryset.filter(collection_id=collection_id)  
      return queryset
        

   def get_serializer_class(self, *args, **kwargs):
      return Serializer.ProductSerializer
   
   def get_serializer_context(self):
      return {'request': self.request}
 
   def destroy(self, request, *args, **kwargs):
       product_object = get_object_or_404(Product, pk=kwargs['pk'])
       orderItem_product_count = product_object.orderitems.count()
       print(orderItem_product_count)
       if orderItem_product_count > 0:
             return Response({'error':f'This Product Can not be delete, There are {orderItem_product_count} items ordered'})
       return super().destroy(request, *args, **kwargs)


# ORDER VIEW SECTION #
class OrderView(ModelViewSet):
    serializer_class = Serializer.OrderSerializer
    http_method_names = [
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "trace",
    "connect"
     ]

    # Adding the permisiion class #
    def get_permissions(self):
        if self.request.method in ['PUT', 'UPDATE','PATCH','DELETE']:
             print("ADMIN PERMISION ORDER")
             return [permissions.IsAdminUser()] # Always return an object
        return [permissions.IsAuthenticated()]

    # Overwrite the create method form (ModelViewSet)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        order_serializer = self.perform_create(serializer)

        OrderSerializer = Serializer.OrderSerializer(order_serializer)
        return Response(OrderSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Overwrite the perform_create method form (ModelViewSet) Adding the return
    def perform_create(self, serializer):
      return  serializer.save()

    def get_queryset(self):
        user_type = self.request.user
        user_id = Customer.objects.values('id').get(user_id=user_type.id)

        # if the user is not part of the staff then data-user-only 
        if not user_type.is_staff: 
            return Order.objects.filter(customer_id=user_id['id'])
        
        # if the user is staff then retrunn all the data-list
        return Order.objects.all()
     
    def get_serializer_class(self):
        # IF THE REQUEST METHOD IS EQUAL TO POST
        if self.request.method == "POST":
            print("Posting Action...")
            return Serializer.OrderCreateSerializer
        return Serializer.OrderSerializer

    def get_serializer_context(self):
       return {
          'request': self.request,
          'get_user_id':self.request.user.id
       }
 
# REVIEW VIEW SECTION #
class ReviewModelVIew(ModelViewSet):
    
    def get_queryset(self):
        print("performing view action....")
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
     
    def get_serializer_class(self):
       return Serializer.ReviewSerializer
    
    def get_serializer_context(self):
       return {
          'product_id': self.kwargs['product_pk'],
          'request':self.request.FILES
       }

class ImgViewProduct(ModelViewSet):
    def get_queryset(self):
        print("Ivoking img Requ3wts")
        return  productImg.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_class(self):        
       if self.request.method == 'GET':  
         print("Data Request GET")
         return Serializer.ProductImgSerializer
       
       elif self.request.method == 'POST':
         print("Data Request Post")
         return Serializer.ProductPostImgSerializer
    
    def get_serializer_context(self):
       return {
                'product_id': self.kwargs['product_pk'],
                'request': self.request
             }
    # Overwrite the create method form (ModelViewSet)
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     headers = self.get_success_headers(serializer.data)
    #     order_serializer = self.perform_create(serializer)
    #     print(serializer)

    #     return Response('ok',status=status.HTTP_201_CREATED, headers=headers)
    



# CART SECTION # 
class CartModelVIew(ModelViewSet):
    
    queryset= Cart.objects.prefetch_related('cartitems__product').all() 
    serializer_class = Serializer.CartSerializer
   
    def get_serializer_context(self):
       return {
          'request': self.request,
       }
    


# CART ITEMS # 
class CartItemsModelVIew(ModelViewSet):
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').all().filter(cart_id=self.kwargs['cart_pk'])
   
    def get_serializer_class(self):
        print(self.request.user) # admin
        if self.request.method =='POST':
           return Serializer.CartItemsSerializerPost
        elif self.request.method == 'PUT':
           return Serializer.CartItemsSerializerPatch
        return Serializer.CartItemsSerializer

    def get_serializer_context(self):
       return {
          'request': self.request,
          'uui_id': self.kwargs['cart_pk']
       }


# Customer Model view #
class CustomerView(ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = Serializer.CustomerSerializer
    permission_classes = [permisionCustom.DjanggoObjectsPermisions]
    
    @action(detail=False, permission_classes=[permisionCustom.HasPermissionHitory])
    def history(self, req:Request):
      return Response("DONE")

    @action(detail=False, methods=['GET','PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, req:Request):
         print(req.user.id)
         if req.user.id == None:
             return Response("NO VALIDATION", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION) 
         (user, created) = Customer.objects.get_or_create(user_id =req.user.id)
         if req.method == 'GET':
           ser = Serializer.CustomerSerializer(user)
           return Response(ser.data, status=status.HTTP_200_OK)
         if req.method == 'PUT':
           ser = Serializer.CustomerSerializer(user, data=req.data)
           ser.is_valid(raise_exception=True)
           ser.save()
           return Response(ser.data, status=status.HTTP_201_CREATED)
         

         
from django.shortcuts import render
from django.core.mail import send_mail
from .tasks import send_emails_notification 
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from requests import get
import logging

logger = logging.getLogger(__name__) # Capturing from __name___

# def action_hello(req:Request):
#     KEY_CACHE = "httpbin"
#     main_objsct =  Product.objects.select_related('collection').prefetch_related('imgs').all()
#     print(main_objsct)
#     if not cache.get(KEY_CACHE):
#         print("FROM CACHE")
#         # store cache informaction #
#         request = get('https://httpbin.org/delay/2')
#         response = request.json()
#         cache.set(KEY_CACHE, response, timeout=60) # data will be store for 60 seconds
#     return render(req, 'hello.html', {'name':cache.get(KEY_CACHE)})

def action_hello(req:Request):
    logger.info("Load http")
    request = get('https://httpbin.org/delay/2')
    response = request.json()
    return render(req, 'hello.html', {'name':response})