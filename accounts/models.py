from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone_no = models.IntegerField(null= True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Address(models.Model):

    reciever_name = models.CharField(max_length=25)
    phone_no = models.IntegerField()
    house_no = models.IntegerField()
    street = models.CharField(max_length=150)
    is_primary = models.BooleanField(default=False)
    landmark = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')






