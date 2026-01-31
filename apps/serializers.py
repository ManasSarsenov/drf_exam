from django.contrib.auth.hashers import make_password
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer
from apps.models import User, ProductImage, Product, CartItem


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductImageCreateSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']


class ProductListModelSerializer(DynamicFieldsModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller = StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'category', 'seller', 'images']


class ProductCreateModelSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'category', 'images']


class UserChangePasswordModelSerializer(ModelSerializer):
    old_password = CharField(max_length=255)
    confirm_password = CharField(max_length=255)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'confirm_password']

    def validate(self, attrs: dict):

        for i in set(self.Meta.fields):
            if i not in attrs:
                raise ValidationError(f"{i} field is required")

        old_password = attrs.get('old_password')
        confirm_password = attrs.get('confirm_password')
        password = attrs.get('password')
        user = self.context['request'].user

        if not user.check_password(old_password):
            raise ValidationError("Old password is not correct")

        if password == old_password:
            raise ValidationError('Passwords are the same ')
        attrs['password'] = make_password(attrs['password'])

        if password != confirm_password:
            raise ValidationError('Passwords do not match')

        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('old_password', None)
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)


class CartItemModelSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = 'id', 'product', 'quantity'
        extra_kwargs = {
            'quantity': {'read_only': True},
            'product': {'write_only': True}
        }
