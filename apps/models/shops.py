from django.db.models import Model, CASCADE, ForeignKey
from django.db.models.fields import CharField


class Seller(Model):
    name = CharField(max_length=255)
    owner = ForeignKey('apps.User', CASCADE, related_name='sellers')
