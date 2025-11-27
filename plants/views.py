from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Plant, Country


def plant_list_view(request):
    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")
    country_id = request.GET.get("country")  # filter by country

    plants = Plant.objects.all()
    countries = Country.objects.all()

    if category:
        plants = plants.filter(category=category)

    if is_edible == "true":
        plants = plants.filter(is_edible=True)

    if country_id:
        plants = plants.filter(countries__id=country_id)

    context = {
        "plants": plants.distinct(),
        "selected_category": category,
        "selected_is_edible": is_edible,
        "countries": countries,
        "selected_country_id": country_id,
    }
    return render(request, "plants/plant_list.html", context)


def plant_detail_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    related_plants = (
        Plant.objects.filter(category=plant.category)
        .exclude(pk=plant.pk)
        .distinct()[:4]
    )

    context = {
        "plant": plant,
        "related_plants": related_plants,
    }
    return render(request, "plants/plant_detail.html", context)


def plant_create_view(request):
    if request.method == "POST":
        plant = Plant.objects.create(
            name=request.POST.get("name"),
            about=request.POST.get("about"),
            used_for=request.POST.get("used_for"),
            image=request.FILES.get("image"),
            category=request.POST.get("category"),
            is_edible=bool(request.POST.get("is_edible")),
        )

        # ربط الدول (اختيار أكثر من دولة)
        country_ids = request.POST.getlist("countries")
        if country_ids:
            plant.countries.set(country_ids)

        # رسالة نجاح
        messages.success(request, "تم إضافة النبتة بنجاح ✅")
        return redirect("plants:plant_detail", pk=plant.pk)

    countries = Country.objects.all()
    context = {"plant": None, "countries": countries}
    return render(request, "plants/plant_form.html", context)


def plant_update_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        plant.category = request.POST.get("category")
        plant.is_edible = bool(request.POST.get("is_edible"))
        plant.save()

        country_ids = request.POST.getlist("countries")
        plant.countries.set(country_ids)

        messages.success(request, "Plant added successfully")
        return redirect("plants:plant_detail", pk=plant.pk)

    countries = Country.objects.all()
    context = {
        "plant": plant,
        "countries": countries,
    }
    return render(request, "plants/plant_form.html", context)


def plant_delete_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == "POST":
        plant.delete()
        messages.error(request, "Plant deleted successfully")
        return redirect("plants:all_plants")

    context = {"plant": plant}
    return render(request, "plants/plant_confirm_delete.html", context)


def plant_search_view(request):
    query = request.GET.get("q", "")
    plants = Plant.objects.all()

    if query:
        plants = plants.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
        )

    context = {
        "plants": plants.distinct(),
        "query": query,
    }
    return render(request, "plants/plant_search.html", context)


def country_plants_view(request, pk):
    country = get_object_or_404(Country, pk=pk)
    plants = Plant.objects.filter(countries=country).distinct()

    context = {
        "country": country,
        "plants": plants,
    }
    return render(request, "plants/country_plants.html", context)
