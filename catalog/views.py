from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DealerRegistrationForm
from .models import AuthorizedDealer, InstrumentFamily, Product


def home(request):
    featured = Product.objects.filter(is_published=True, is_featured=True)[:6]
    hero_product = Product.objects.filter(is_published=True, main_image__isnull=False).first()
    return render(request, "catalog/home.html", {"featured": featured, "hero_product": hero_product})


def product_list(request):
    products = Product.objects.filter(is_published=True)
    family = request.GET.get("family", "")
    if family in InstrumentFamily.values:
        products = products.filter(family=family)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(model_number__icontains=query) | Q(short_description__icontains=query)
        )
    return render(request, "catalog/product_list.html", {
        "products": products, "families": InstrumentFamily.choices, "active_family": family, "query": query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_published=True)
    return render(request, "catalog/product_detail.html", {"product": product})


def dealer_finder(request):
    dealers = AuthorizedDealer.objects.filter(is_active=True)
    return render(request, "catalog/dealer_finder.html", {"dealers": dealers})


def dealer_registration(request):
    if request.method == "POST":
        form = DealerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. We have received your dealer registration request.")
            return redirect("catalog:dealer_registration")
    else:
        form = DealerRegistrationForm()
    return render(request, "catalog/dealer_registration.html", {"form": form})
