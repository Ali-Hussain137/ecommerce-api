from gzip import READ
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.core import validators
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    discount = models.BooleanField(default=False)
    image = CloudinaryField('image')
    token = models.CharField(null=True, blank=True, max_length=1200)
    confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(validators=[validators.MinValueValidator(0)])
    quantity = models.IntegerField(
        validators=[validators.MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart, through="ProductCart")
    order = models.ManyToManyField(Order, through="ProductOrder")

    def __str__(self):
        return self.product_name


class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[validators.MinValueValidator(1)], default=1
    )

    def __str__(self):
        return self.product.product_name


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[validators.MinValueValidator(1)], default=1
    )
    subtotal = models.IntegerField(
        validators=[validators.MinValueValidator(0)])


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Comment(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Image(models.Model):
    image = CloudinaryField('image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

