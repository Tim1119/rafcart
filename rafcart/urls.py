from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('account/',include('apps.account.urls',namespace='account')),
    path('profiles/',include('apps.profiles.urls',namespace='profiles')),
    path('product/',include('apps.product.urls',namespace='product')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

