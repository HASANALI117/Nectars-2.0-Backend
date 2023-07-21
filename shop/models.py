from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


USER_TYPE_CHOICES = (
    ('customer', 'Customer'),
    ('admin', 'Admin'),
    ('shop_owner', 'Shop Owner'),
)

#extend the user model
class Custom_User(AbstractUser):
    userType=models.CharField(max_length=20,default='customer',choices=USER_TYPE_CHOICES,verbose_name='User Type')
    shopId=models.ForeignKey("shop.Shop", verbose_name="Shop ID", on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.userType == 'admin':
            self.shopId = None
        super().save(*args, **kwargs)


class Shop(models.Model):
    shopId = models.AutoField(primary_key=True)
    shopName = models.CharField(
        max_length=100, unique=True, 
        verbose_name=("Shop Name"), 
        error_messages={'unique':"This shop name is already taken.", 'required':"This field is required."},
        )
    description = models.CharField(
        max_length=100,
        verbose_name=("Description"),
        error_messages={'required':"This field is required."},
        )
    shopOwner = models.ForeignKey("shop.Custom_User", verbose_name=("Shop Owner"), on_delete=models.CASCADE)

    def __str__(self):
        return self.shopName
    
    class Meta:
        verbose_name = ("Shop")
        verbose_name_plural = ("Shops")


class Product(models.Model):
    productId = models.AutoField(primary_key=True, verbose_name=("Product ID"))
    name = models.CharField(
        max_length=100,
        verbose_name=("Product Name"),
        error_messages={'required':"name field is required."},
        )
    description = models.CharField(
        max_length=100,
        verbose_name=("Description"),
        error_messages={'required':"description field is required."},
        )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=("Price"),
        error_messages={'required':"price field is required."},
        )
    shopId = models.ForeignKey("shop.Shop", verbose_name=("Shop ID"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")
    
    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")





