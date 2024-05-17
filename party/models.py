from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator 

# Create your models here.
print("Party MODEL")
class Users(AbstractUser):
      email = models.EmailField(unique=True)     
      username_validator = UnicodeUsernameValidator()
      lat = models.CharField(max_length=24, blank=True, null=True)

      username = models.CharField(
            _("username"),
            max_length=150,
            unique=True,
            help_text=_(
                  "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. and @username"
            ),
            validators=[username_validator],
            error_messages={
                  "unique": _("A user with that username already exists."),
            },
      )

