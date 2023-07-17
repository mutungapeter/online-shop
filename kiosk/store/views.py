from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Variation
from category.models import Category
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from orders.models import OrderProduct
from .models import ReviewRating, ProductGallery
from .forms import ReviewForm, ProductForm, GalleryForm, VariationForm
# Create your views here.
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger


def store(request, category_slug=None):
    categories = None
    products=None

    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count() 
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        "products":  paged_products ,
        'product_count': product_count
        }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except Exception:
            orderproduct = None
    else:
        orderproduct = None
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        "product_gallery":  product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = Product.objects.none()
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, "store/store.html", context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save() 
            gallery_images = request.FILES.getlist("gallery_images")
            for image in gallery_images:
                ProductGallery.objects.create(product=product, image=image)
            messages.success(request, "Product added successfully.")
            return redirect("products")
    else:
        form = ProductForm()
    context = {
        "form": form,
    }
    return render(request, "store/add_product.html", context)




def products(request):
    products_list = Product.objects.all()
    context = {
    "products_list": products_list,
}
    return render(request, "store/products_list.html", context)


def add_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save() 
            messages.success(request, "Product gallery added successfully.")
            return redirect("product_gallery")
    else:
        form = GalleryForm()
    context = {
        "form": form,
    }
    return render(request, "store/add_product_gallery.html", context)




def product_gallery(request):
    products_gallery = ProductGallery.objects.all()
    context = {
    "products_gallery": products_gallery,
}
    return render(request, "store/products_gallery.html", context)



def add_variation(request):
    if request.method == "POST":
        form = VariationForm(request.POST, request.FILES)
        if form.is_valid():
            variation = form.save() 
            messages.success(request, "Product Variation added successfully.")
            return redirect("product_variation")
    else:
        form = VariationForm()
    context = {
        "form": form,
    }
    return render(request, "store/add_product_variation.html", context)




def product_variation(request):
    product_variations = Variation.objects.all()
    context = {
    "product_variations": product_variations,
}
    return render(request, "store/product_variations.html", context)

