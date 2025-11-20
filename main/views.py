from django.shortcuts import render, redirect
from .models import Contact


def home_view(request):
    return render(request, "main/home.html")


def contact_view(request):
    if request.method == "POST":
        Contact.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )
        return redirect("main:contact")

    return render(request, "main/contact.html")


def contact_messages_view(request):
    messages = Contact.objects.order_by("-created_at")
    context = {"messages": messages}
    return render(request, "main/contact_messages.html", context)
