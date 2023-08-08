from django.contrib import admin
from .models import Product, Category, Domain, Brand


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_filter = ('name',)

    list_display = (
        'id',
        'name',
        'domain',
    )

    search_fields = (
        'domain',
        'name',
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_filter = ('name',)

    list_display = (
        'id',
        'name'
    )
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_filter = ('sku',)

    list_display = (
        'id',
        'name',
        'category',
        'brand',
    )

    search_fields = (
        'name',
    )
