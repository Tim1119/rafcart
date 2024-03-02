from django.shortcuts import render,get_object_or_404
from django.views.generic import UpdateView,TemplateView,ListView,DetailView
from .models import Product,Category,Brand
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models import Q
from django.db import models
# Create your views here.
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'product/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get top 6 categories with highest number of product
        categories = Category.objects.annotate(num_products=Count('products')).order_by('-num_products')[:6] 
        top_new_arrivals = Product.objects.all().order_by('-created_on')[:4]
        recommended_for_you = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews').exclude(Q(id__in=[product.id for product in top_new_arrivals]))[:8]
        context['categories'] = categories
        context['top_new_arrivals'] = top_new_arrivals
        context['recommended_for_you'] = recommended_for_you
        return context

class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name='product'

class ShopView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'product/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories =  Category.objects.annotate(product_count=models.Count('products'))
        brands = Brand.objects.annotate(product_count=Count('product'))
        products = Product.objects.all()
        brands_count = Brand.objects.all().count()
        categories_count =Category.objects.all().count()

        active_category = self.request.GET.get('category', '')
        if active_category:
            products = products.filter(category__slug=active_category)

        active_brand = self.request.GET.get('brand', '')
        if active_brand:
            products = products.filter(brand__slug=active_brand)

        query = self.request.GET.get('query', '')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(details__icontains=query))

        context['brands'] = brands
        context['brands_count'] = brands_count
        context['categories_count'] = categories_count
        context['categories'] = categories
        context['products'] = products
        return context

def search_shop(request):
    categories = Category.objects.annotate(product_count=models.Count('products'))
    brands = Brand.objects.annotate(product_count=Count('product'))
    brands_count = Brand.objects.all().count()
    categories_count = Category.objects.all().count()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
        'active_category': active_category,
        'brands_count':brands_count,
        'categories_count':categories_count
    }

    return render(request, 'product/shop.html', context)
