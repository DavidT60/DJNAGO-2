from rest_framework_nested import routers
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(
    'collection',
    views.CollectionModelView
)

router.register(
    'product',
    views.ProductModelView,
    basename='product'
)

router.register(
    'order',
    views.OrderView,
    basename='order'
)



router.register(
    'cart',
    views.CartModelVIew,
    basename='cart'
)


router.register(
    'customer',
    views.CustomerView,
    basename='customer'
)



# Product Nested Router #
domains_router_product= routers.NestedSimpleRouter(router, r'product', lookup='product')
domains_router_product.register(r'reviews', views.ReviewModelVIew, basename='product-reviews')

# Cart Nested Router 

domains_router_cart = routers.NestedSimpleRouter(router, r'cart', lookup='cart')
domains_router_cart.register(r'cartitems', views.CartItemsModelVIew, basename='cart-reviews')


# URLConf
urlpatterns = [
    path('',include(router.urls)),
    path('',include(domains_router_product.urls)),
    path('',include(domains_router_cart.urls)),

] 
# print(urlpatterns)
# print(router.urls)
