from django.db import models
from autoslug import AutoSlugField
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    facebook_url = models.URLField(blank=True,null=True)
    twitter_url = models.URLField(blank=True,null=True)
    instagram_url = models.URLField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Product Brand'
        verbose_name_plural = 'Product Brands'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(upload_to='category-images', processors=[ResizeToFill(1540, 960)], format='JPEG', options={'quality': 70})

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)
    
    @property
    def get_category_image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

class Product(models.Model):

    class Color(models.TextChoices):
        Pink = "Pink", _("Pink")
        Black = "Black", _("Black")
        White = "White", _("White")

    class Size(models.TextChoices):
        XS = "XS", _("XS")
        S = "S", _("S")
        M = "M", _("M")
        L = "L", _("L")
        XL = "XL", _("XL")

    class Material(models.TextChoices):
        Latex = "Latex", _("Latex")
        Memory_Foam = "Memory_Foam", _("Memory_Foam")
        Polyurethane_Foam  = "Polyurethane_Foam ", _("Polyurethane_Foam ")
        Polyester_Fiberfill = "Polyester_Fiberfill", _("Polyester_Fiberfill")

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255,choices=Color.choices,default=Color.Black)
    material = models.CharField(max_length=255,choices=Material.choices,default=Material.Latex)
    size = models.CharField(max_length=255,choices=Size.choices,default=Size.M)
    price = models.IntegerField()
    weight = models.IntegerField(blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    thumbnail = ProcessedImageField(upload_to='product-images', processors=[ResizeToFill(1080, 800)], format='JPEG', options={'quality': 70})
    image2 = ProcessedImageField(upload_to='product-images', processors=[ResizeToFill(1080, 800)], format='JPEG', options={'quality': 70})
    image3 = ProcessedImageField(upload_to='product-images', processors=[ResizeToFill(1080, 800)], format='JPEG', options={'quality': 70})
    image4 = ProcessedImageField(upload_to='product-images', processors=[ResizeToFill(1080, 800)], format='JPEG', options={'quality': 70})
    image5 = ProcessedImageField(upload_to='product-images', processors=[ResizeToFill(1080, 800)], format='JPEG', options={'quality': 70},blank=True,null=True)

    class Meta:
        ordering = ('-created_on',)
    
    def __str__(self):
        return self.name

    def get_related_products(self, num_products=4):
        if self.category:
            # If the product has a category, get four products from the same category
            related_products = Product.objects.filter(category=self.category).exclude(id=self.id).order_by('?')[:num_products]
        else:
            # If the product doesn't have a category, get four random products
            related_products = Product.objects.exclude(id=self.id).order_by('?')[:num_products]
        return related_products

    @property
    def get_thumbnail_url(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url
    
    @property
    def get_second_thumbnail_url(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    @property
    def get_third_thumbnail_url(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    
    @property
    def get_fourth_thumbnail_url(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url
    
    @property
    def get_fifth_thumbnail_url(self):
        try:
            url = self.image5.url
        except:
            url = ''
        return url


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

