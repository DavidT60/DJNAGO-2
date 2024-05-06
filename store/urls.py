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


domains_router = routers.NestedSimpleRouter(router, r'product', lookup='product')
domains_router.register(r'reviews', views.ReviewModelVIew, basename='product-reviews')


# URLConf
urlpatterns = [
    path('',include(router.urls)),
    path('',include(domains_router.urls)),

] 
print(urlpatterns)
print(router.urls)
