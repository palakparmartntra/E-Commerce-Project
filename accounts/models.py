from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """ model for user details """

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone_no = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    """model for user address """

    receiver_name = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=10)
    house_no = models.CharField(max_length=8)
    street = models.CharField(max_length=150)
    is_primary = models.BooleanField(default=False)
    landmark = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
