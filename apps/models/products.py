from django.db.models import CASCADE, ForeignKey
from django.db.models.fields import CharField, PositiveIntegerField, PositiveSmallIntegerField, TextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.models.base import SlugBaseModel, ImageBaseModel, CreatedBaseModel


class Category(SlugBaseModel, ImageBaseModel, MPTTModel):
    name = CharField(max_length=255)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Product(SlugBaseModel, CreatedBaseModel):
    name = CharField(max_length=255)
    price = PositiveIntegerField()
    discount = PositiveSmallIntegerField(default=0)
    quantity = PositiveIntegerField(default=0)  # Ombordagi soni
    description = TextField(blank=True)
    seller = ForeignKey('apps.Seller', CASCADE, related_name='products')
    category = ForeignKey('apps.Category', CASCADE, related_name='products')


class ProductImage(ImageBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
