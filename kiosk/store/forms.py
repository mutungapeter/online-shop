from django import forms
from.models import ReviewRating, Product, ProductGallery, Variation
from category.models import Category

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review','rating']
        
        
        
class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False, error_messages= {"invalid": ("Image files only")}, widget=forms.FileInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, widget=forms.Select(attrs={"class": "form-control"}))
    is_available = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput())
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    gallery_images = forms.ImageField(required=False, widget=forms.FileInput(attrs={"multiple": True}))
    class Meta:
        model = Product
        fields = ["product_name", "slug", "description", "price","images", "stock", "is_available","category", "gallery_images"]
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ="form-control" 


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"multiple": True}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, widget=forms.Select(attrs={"class": "form-control"}))
    class Meta:
        model = ProductGallery
        fields = ["product", "image"]
        
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ="form-control" 

variation_category_choices = (
    ("color", "Color"),
    ("size", "Size")
)
class VariationForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, widget=forms.Select(attrs={"class": "form-control"}))
    variation_category = forms.ChoiceField(choices=variation_category_choices, required=True, widget=forms.Select(attrs={"class": "form-control"}))
    is_active = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput())
    class Meta:
        model = Variation
        fields = ["product", "variation_category", "variation_value", "is_active", ]
        
    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ="form-control" 

