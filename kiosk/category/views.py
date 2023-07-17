from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import CategoryForm
# Create your views here.
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            slug = form.cleaned_data["slug"]
            description = form.cleaned_data["description"]
            cat_image = form.cleaned_data["cat_image"]
            category = Category.objects.create(category_name=category_name, slug=slug, description=description, cat_image=cat_image)
            category.save()
            messages.success(request, "Category  added successfully.")
            return redirect("categories")
    else:
        form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "category/add_category.html", context)

def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "category/categories.html", context)

