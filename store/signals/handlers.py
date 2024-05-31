from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import customer_order_created
from .. import models


# When we create a post in sender (module), it will trigger #
@receiver([post_save],sender=settings.AUTH_USER_MODEL)
def create_refer_in_customer_with_userid(sender,**kwargs):
    print("Trigging signal")
    print(kwargs)
    USERT_INSTANCE = kwargs['instance']
    print(USERT_INSTANCE)
    if kwargs['created']:
        models.Customer.objects.create(user=kwargs['instance'])
        

@receiver(customer_order_created) # Suscribing this handler #
def create_an_order(sender, **kwargs):
    print("Trigging signal")
    print(kwargs)
    pass