from django.contrib import admin
from .models import Plant, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible", "countries")
    search_fields = ("name", "about", "used_for")
    filter_horizontal = ("countries",)
