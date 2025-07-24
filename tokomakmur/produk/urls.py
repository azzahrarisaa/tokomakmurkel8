from django.contrib import admin
from django.urls import path
from produk.views import beranda
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', beranda, name='beranda'),
    path('', include('produk.urls')),  # ini perlu include yang benar
]