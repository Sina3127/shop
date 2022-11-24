from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from unicodedata import category

from shop.models import Product, Category, ReviewComment, Cart, Banner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'details']
    list_filter = ['category', 'last_update']
    search_fields = ['title']
    autocomplete_fields = ['category']
    def details(self, product):
        url = reverse('itemDetails', args=(product.id,))
        return format_html('<a href="{}"> details </a>', url)
admin.site.register(ReviewComment)
admin.site.register(Cart)
admin.site.register(Banner)