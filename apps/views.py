from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.filters import ProductFilterSet
from apps.models import User, ProductImage, Product, CartItem, Cart
from apps.serializers import UserChangePasswordModelSerializer, ProductImageCreateSerializer, \
    ProductListModelSerializer, ProductCreateModelSerializer, CartItemModelSerializer


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass
    # serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['users'])
class UserChangePasswordUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordModelSerializer
    permission_classes = IsAuthenticated,
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True})


@extend_schema(tags=['users'])
class CartItemListAPIView(ListCreateAPIView):
    queryset = CartItem.objects.select_related('product', 'product__seller').prefetch_related('product__images')
    serializer_class = CartItemModelSerializer
    pagination_class = None
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)


@extend_schema(tags=['products'])
class ProductImageCreateAPIView(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer


@extend_schema(tags=['products'])
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductListModelSerializer
    filter_backends = DjangoFilterBackend,
    filterset_class = ProductFilterSet

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = ProductCreateModelSerializer
        return super().get_serializer_class()


# class IsAuthenticated(BasePermission):
#     """
#     Allows access only to authenticated users.
#     """
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)

# class BasePermission(metaclass=BasePermissionMetaclass):
#     """
#     A base class from which all permission classes should inherit.
#     """
#
#     def has_permission(self, request, view):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True

class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

        if request.method in SAFE_METHODS:
            return True
        return obj.seller.owner == request.user


@extend_schema(tags=['products'])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    permission_classes = IsAuthenticated, IsProductOwner,
    http_method_names = ['get', 'post', 'patch', 'delete']
