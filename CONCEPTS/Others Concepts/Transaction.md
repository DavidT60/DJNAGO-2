 # Transaction in Django #

 A database transaction is a unit of work that ensures all database operations within it are treated as a single entity. This means either all the operations succeed, or none of them are applied. This guarantees data consistency and prevents partial updates that could leave your database in an inconsistent state.

 What does means Inconsistent State?

 ```.py 
   class OrderCreateSerializer(serializers.Serializer):
     cart_id = serializers.UUIDField()

     def save(self, **kwargs):

          cart_id = self.validated_data['cart_id'] # Get the cart id
          get_user_id = self.context['user_id'] # get the user id form customer 
        
          # Getting Customer from User id  #
          (customer, created) = models.Customer.objects.get_or_create(usser_id=get_user_id)
     
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
 ```
 Let's take a look. In the transaction above, we have different actions: `getting` and `creating` from the database. If something wrong happens (server off) while this transaction is executed, e.g., creating the order row (# Create Order Table #), it will just end with an order that is not related to any orderitems and we end up with inconsistent data because the other part of the transaction was not executed.

 For that is used `transaction.atomic`:
# transaction.atomic Context Manager:#
Django provides the transaction.atomic context manager from the django.db module to manage database transactions within your code. It simplifies transaction handling by automatically:

*Starting a transaction*: When you enter the with block using transaction.atomic, a transaction is automatically started.

*Committing the transaction*: If no exceptions occur within the with block, the transaction is committed, making the changes permanent in the database.

*Rolling back the transaction*: If an exception occurs within the with block, the entire transaction is rolled back, undoing all database changes made so far. This ensures data integrity and prevents partial updates.