from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required  
from django.utils.text import slugify
# Create your views here.
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            slug = slugify(category_name)
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

@login_required(login_url='login')
def Edit_category(request, pk):
    category = None 
    try:
       category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect("categorie")
        pass

    if request.method == "POST":
        category_form = CategoryForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Your Category has been updated.")
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)
        
    context = {
        "form": form,
        "category": category,
    }
    return render(request, 'category/edit_category.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("categories")

    context = {
        "category": category,
    }
    return render(request, "category/delete_category.html", context)