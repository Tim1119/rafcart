from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid
from phonenumber_field.phonenumber import PhoneNumber
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


User = get_user_model()


# Create your models here.
class Profile(models.Model):

    class Gender(models.TextChoices):
        Male = "Male", _("Male")
        Female = "Female", _("Female")
        Other = "Other", _("Other")

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ProcessedImageField(upload_to='avatars', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    date_of_birth = models.DateField()
    slug = AutoSlugField(populate_from='user', unique=True)
    sex = models.CharField(max_length=255, choices=Gender.choices, default=Gender.Other)
    phone_number = PhoneNumber()
    address = models.TextField(blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return 'This profile is for {self.user.full_name}'


    @property
    def get_avatar_url(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url
