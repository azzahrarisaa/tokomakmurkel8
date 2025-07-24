"""
URL configuration for tokomakmur project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from produk.views import beranda
from produk.views import beranda, dashboard  # pastikan ini
from produk.views import produk
from produk import views  # ini untuk akses views.kategori_produk dll
from django.conf.urls.static import static
from django.conf import settings  # INI WAJIB
from django.urls import path, include
from django.contrib.auth import views as auth_views







urlpatterns = [
    path('admin/', admin.site.urls),
    path('', beranda, name='beranda'),
    path('dashboard/', dashboard, name='dashboard'),
    # urls.py
    path('produk/', views.daftar_produk, name='daftar_produk'),
    path('produk/tambah/', views.tambah_produk, name='tambah_produk'),
    path('produk/edit/<int:id>/', views.edit_produk, name='edit_produk'),
    path('produk/hapus/<int:id>/', views.hapus_produk, name='hapus_produk'),  

    # Kategori, Satuan, Pemasok
    path('kategori/', views.kategori_produk, name='kategori_produk'),
    path('kategori/tambah/', views.tambah_kategori, name='tambah_kategori'),
    path('kategori/edit/<int:id>/', views.edit_kategori, name='edit_kategori'),
    path('kategori/hapus/<int:id>/', views.hapus_kategori, name='hapus_kategori'),

    path('satuan/', views.satuan_produk, name='satuan_produk'),
    path('satuan/tambah/', views.tambah_satuan, name='tambah_satuan'),
    path('satuan/edit/<int:id>/', views.edit_satuan, name='edit_satuan'),
    path('satuan/hapus/<int:id>/', views.hapus_satuan, name='hapus_satuan'),
    
    path('pemasok/', views.daftar_pemasok, name='pemasok'),
    path('pemasok/tambah/', views.tambah_pemasok, name='tambah_pemasok'),
    path('pemasok/edit/<int:id>/', views.edit_pemasok, name='edit_pemasok'),
    path('pemasok/hapus/<int:id>/', views.hapus_pemasok, name='hapus_pemasok'),

    # Penjualan
    path('penjualan/', views.daftar_penjualan, name='penjualan'),
    path('penjualan/tambah/', views.tambah_penjualan, name='tambah_penjualan'),
    path('penjualan/edit/<int:id>/', views.edit_penjualan, name='edit_penjualan'),
    path('penjualan/hapus/<int:id>/', views.hapus_penjualan, name='hapus_penjualan'),
    path('penjualan/detail/<int:id>/', views.detail_penjualan, name='detail_penjualan'),


    # Pembelian
    path('pembelian/', views.daftar_pembelian, name='daftar_pembelian'),
    path('pembelian/tambah/', views.tambah_pembelian, name='tambah_pembelian'),
    path('pembelian/edit/<int:id>/', views.edit_pembelian, name='edit_pembelian'),
    path('pembelian/hapus/<int:id>/', views.hapus_pembelian, name='hapus_pembelian'),
    path('pembelian/detail/<int:id>/', views.detail_pembelian, name='detail_pembelian'),

    path('user/', views.daftar_user, name='daftar_user'),
    path('user/tambah/', views.tambah_user, name='tambah_user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # ⬅ tambahkan ini
    path('user/hapus/<int:user_id>/', views.hapus_user, name='hapus_user'),

]

# Tambahkan ini di bagian bawah urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)