from django.db.models import Model, OneToOneField, CASCADE, ForeignKey
from django.db.models.fields import PositiveIntegerField


class Cart(Model):
    user = OneToOneField('apps.User', CASCADE, related_name='cart')


class CartItem(Model):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='items')
    product = ForeignKey('apps.Product', CASCADE)
    quantity = PositiveIntegerField(default=1)


class Favorite(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='favorites')
    product = ForeignKey('apps.Product', CASCADE, related_name='favored_by')
