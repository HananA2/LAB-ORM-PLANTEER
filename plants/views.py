from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant


def plant_list_view(request):
    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")

    plants = Plant.objects.all()

    if category:
        plants = plants.filter(category=category)

    if is_edible == "true":
        plants = plants.filter(is_edible=True)

    context = {
        "plants": plants,
        "selected_category": category,
        "selected_is_edible": is_edible,
    }
    return render(request, "plants/plant_list.html", context)


def plant_detail_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(pk=plant.pk)[:4]

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
        return redirect("plants:plant_detail", pk=plant.pk)

    return render(request, "plants/plant_form.html")


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

        return redirect("plants:plant_detail", pk=plant.pk)

    context = {"plant": plant}
    return render(request, "plants/plant_form.html", context)


def plant_delete_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == "POST":
        plant.delete()
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
        "plants": plants,
        "query": query,
    }
    return render(request, "plants/plant_search.html", context)
