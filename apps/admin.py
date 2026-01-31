from django.contrib import admin

from apps.models import Category, Product, ProductImage, Seller


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Seller)
class SellerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
