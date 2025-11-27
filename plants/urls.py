from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.plant_list_view, name="all_plants"),
    path("<int:pk>/detail/", views.plant_detail_view, name="plant_detail"),
    path("new/", views.plant_create_view, name="plant_create"),
    path("<int:pk>/update/", views.plant_update_view, name="plant_update"),
    path("<int:pk>/delete/", views.plant_delete_view, name="plant_delete"),
    path("search/", views.plant_search_view, name="plant_search"),
    path("country/<int:pk>/", views.country_plants_view, name="country_plants"),
]
