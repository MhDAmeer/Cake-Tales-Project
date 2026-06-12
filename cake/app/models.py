from django.db import models

import uuid

from django.db.models import Sum

# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4,unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        abstract = True

# class CategoryChoices(models.TextChoices):

#     BIRTHDAY_CAKES = 'Birthday Cakes','Birthday Cakes'

#     WEDDING_CAKES = 'Wedding Cakes','Wedding Cakes'

#     PLUM_CAKES = 'Plim cakes','Plum Cakes'

#     MUFFINS = 'Muffins', 'Muffins'

class Category(BaseClass):

    name = models.CharField(max_length=30)

    class Meta:

        verbose_name = 'Categories'

        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# class FlavourChoices(models.TextChoices):

#     VANILA = 'Vanila','Vanila'

#     BLACK_FOREST = 'Black Forest','Black Forest'

#     WHITE_FOREST = 'White Forest','White Forest'

#     RED_VELVET = 'Red Velvet','Red Velvet'

class Flavour(BaseClass):

    name = models.CharField(max_length=30)

    class Meta:

        verbose_name = 'Flavours'

        verbose_name_plural = 'Flavours'

    def __str__(self):
        return self.name

# class WeightChoices(models.TextChoices):

#     ONE_KG = '1kg','1kg'

#     TWO_KG = '2kg','2kg'

#     FIVE_KG = '5kg','5kg'

class Weight(BaseClass):

    name = models.CharField(max_length=30)

    class Meta:

        verbose_name = 'Weights'

        verbose_name_plural = 'Weights'

    def __str__(self):
        return self.name

# class ShapeChoices(models.TextChoices):

#     CIRCLE = 'Circle','Circle'

#     RECTANGLE = 'Rectangle', 'Rectangle'

#     HEART = 'Heart' , 'Heart'

class Shape(BaseClass):

    name = models.CharField(max_length=30)

    class Meta:

        verbose_name = 'Shapes'

        verbose_name_plural = 'Shapes'

    def __str__(self):
        return self.name


class Cake(BaseClass):

    name = models.CharField(max_length=30)

    description = models.TextField()

    photo = models.ImageField(upload_to='cake-images')

    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    flavour = models.ForeignKey('Flavour',on_delete=models.CASCADE)

    weight = models.ForeignKey('Weight',on_delete=models.CASCADE)

    shape = models.ForeignKey('Shape',on_delete=models.CASCADE)

    egg_added = models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)

    price = models.FloatField()

    class Meta :

        verbose_name = 'cakes'

        verbose_name_plural = 'Cakes'

    def __str__(self):
        return self.name


class Wishlist(BaseClass):

    user = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    cakes = models.ManyToManyField('Cake',blank=True)

    class Meta:

        verbose_name = 'Wishlists'

        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return f'{self.user.username} Wishlist'
    
class Cart(BaseClass):

    user = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    cakes = models.ManyToManyField('Cake',blank=True)
    
    @property
    def get_total(self):

        total = self.cakes.aggregate(total=Sum('price')).get('total')

        return total if total else 0

    class Meta:

        verbose_name = 'Carts'

        verbose_name_plural = 'Carts'

    def __str__(self):

        return f'{self.user.username} Cart'
    
class PaymentOptionChoices(models.TextChoices):

    COD = 'COD','COD'

    ONLINE = 'Online','Online'

class DeliveryAddress(BaseClass):

    user = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)

    house_num_or_building_name = models.CharField(max_length=20)

    landmark = models.CharField(max_length=20)

    place = models.CharField(max_length=20)

    pincode = models.CharField(max_length=6)

    class Meta:

        verbose_name = 'Delivery Address'

        verbose_name_plural = 'Delivery Address'

    def __str__(self):

        return f'{self.user.username} Delivery Address'

class Order(BaseClass):

    user = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)

    order_id = models.CharField(max_length=10)

    cakes = models.ManyToManyField('Cake')

    total_price = models.FloatField()

    payment_option = models.CharField(max_length=10,choices=PaymentOptionChoices.choices,null=True,blank=True)

    delivery_address = models.ForeignKey('DeliveryAddress',on_delete=models.SET_NULL,null=True,blank=True)

    order_placed = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Orders'

        verbose_name_plural = 'Orders'

    def __str__(self):

        return f'{self.user.username} {self.order_id}'

