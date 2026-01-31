from django.urls import path

from apps.views import CustomTokenObtainPairView, CustomTokenRefreshView, UserChangePasswordUpdateAPIView, \
    ProductListCreateAPIView, ProductViewSet

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:pk>',
         ProductViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})),

    path('users/change-password/', UserChangePasswordUpdateAPIView.as_view(), name='users_change_password'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),

]
