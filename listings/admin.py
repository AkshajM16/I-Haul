from django.contrib import admin
from .models import Category, Listing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_sold", "seller", "created_at")
    list_filter = ("category", "is_sold", "created_at")
    search_fields = ("title", "description", "seller__username")