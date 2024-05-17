from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.contenttypes.admin import GenericTabularInline

# from store.models import Product
# from store.admin import ProductAdmin

# from tags.models import TaggedItem

from . import models


@admin.register(models.Users)
class SuperUser(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem


# class CustomProductAdmin(ProductAdmin):
#     inlines = [TagInline]


# admin.site.unregister(Product)
# admin.site.register(Product, CustomProductAdmin)