from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

USER_TYPE_CHOICES = (
    ("customer", "Customer"),
    ("admin", "Admin"),
    ("shop_owner", "Shop Owner"),
)


# extend the user model
class Custom_User(AbstractUser):
    userType = models.CharField(
        max_length=20,
        default="customer",
        choices=USER_TYPE_CHOICES,
        verbose_name="User Type",
    )
    shopId = models.ForeignKey(
        "shop.Shop",
        verbose_name="Shop ID",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.userType == "admin":
            self.shopId = None
        super().save(*args, **kwargs)


class Shop(models.Model):
    shopId = models.AutoField(primary_key=True)
    shopName = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=("Shop Name"),
        error_messages={
            "unique": "This shop name is already taken.",
            "required": "This field is required.",
        },
    )
    description = models.CharField(
        max_length=100,
        verbose_name=("Description"),
        error_messages={"required": "This field is required."},
    )
    shopOwner = models.ForeignKey(
        "shop.Custom_User", verbose_name=("Shop Owner"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.shopName

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"


class ShopProps(models.Model):
    shopPropsId = models.AutoField(primary_key=True)
    shopId = models.ForeignKey(
        "shop.Shop",
        verbose_name=("Shop ID"),
        on_delete=models.CASCADE,
        error_messages={"required": "This field is required."},
    )
    props = models.JSONField(
        default=dict,
        verbose_name=("Shop Properties"),
        error_messages={"required": "This field is required."},
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Shop Property"
        verbose_name_plural = "Shop Properties"


class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=("Category Name"),
        error_messages={
            "unique": "This category name is already taken.",
            "required": "This field is required.",
        },
    )
    description = models.CharField(
        max_length=100,
        verbose_name=("Description"),
        error_messages={"required": "This field is required."},
    )
    shopId = models.ForeignKey(
        "shop.Shop", verbose_name=("Shop ID"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    productId = models.AutoField(primary_key=True, verbose_name=("Product ID"))
    name = models.CharField(
        max_length=100,
        verbose_name=("Product Name"),
        error_messages={"required": "name field is required."},
    )
    description = models.CharField(
        max_length=100,
        verbose_name=("Description"),
        error_messages={"required": "description field is required."},
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=("Price"),
        error_messages={"required": "price field is required."},
    )
    poster_image_url = models.URLField(
        max_length=200,
        verbose_name=("Poster Image URL"),
        error_messages={"required": "poster_image_url field is required."},
        blank=True,
        null=True,
    )
    image_urls = models.JSONField(
        default=list, verbose_name=("Image URLs"), blank=True, null=True
    )
    shopId = models.ForeignKey(
        "shop.Shop", verbose_name=("Shop ID"), on_delete=models.CASCADE
    )
    categoryId = models.ForeignKey(
        "shop.Category",
        verbose_name=("Category ID"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")


class Cart(models.Model):
    products = JSONField(default=list, blank=True)
    userId = models.ForeignKey(
        "shop.Custom_User", verbose_name=("User ID"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.userId) + " Cart"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def clean(self):
        for product in self.products:
            if product["quantity"] <= 0:
                raise ValidationError("Quantity must be greater than zero.")


# Signal to create a new cart for a new customer user
@receiver(post_save, sender=Custom_User)
def create_cart_for_new_customer(sender, instance, created, **kwargs):
    print("Signal called")
    if created and instance.userType == "customer":
        cart = Cart.objects.create(userId=instance)
        cart.save()


# # Signal to create a new shop for a new shop owner user
# @receiver(post_save, sender=Custom_User)
# def create_shop_for_new_shop_owner(sender, instance, created, **kwargs):
#     if created and instance.userType == 'shop_owner':
#         with transaction.atomic():
#             shop = Shop.objects.create(shopOwner=instance)
#             instance.shopId = shop.shopId
#             instance.save()


# signal to update the shopId of the shop owner user when a new shop is created
@receiver(post_save, sender=Shop)
def update_shopId_for_shop_owner(sender, instance, created, **kwargs):
    print("Shop Signal called")
    if created:
        user = Custom_User.objects.get(id=instance.shopOwner.id)
        user.shopId = instance
        user.save()
