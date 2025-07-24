from django.contrib import admin
from .models import (
    KategoriProduk, Satuan, Pemasok, Produk,
    Pembelian, DetailPembelian,
    Penjualan, DetailPenjualan
)

# === Admin untuk KategoriProduk ===
@admin.register(KategoriProduk)
class KategoriProdukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'deskripsi')
    search_fields = ('nama',)


# === Admin untuk Satuan ===
@admin.register(Satuan)
class SatuanAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)


# === Admin untuk Pemasok ===
@admin.register(Pemasok)
class PemasokAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kontak', 'alamat')
    search_fields = ('nama', 'kontak')
    list_filter = ('nama',)


# === Admin untuk Produk ===
@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('kode_produk', 'nama', 'kategori', 'stok', 'satuan', 'harga_beli', 'harga_jual', 'pemasok')
    search_fields = ('kode_produk', 'nama')
    list_filter = ('kategori', 'satuan', 'pemasok')
    list_editable = ('stok', 'harga_jual')
    # readonly_fields = ('kode_produk',)
    fieldsets = (
        (None, {
            'fields': ('kode_produk', 'nama', 'kategori', 'satuan', 'pemasok')
        }),
        ('Harga & Stok', {
            'fields': ('stok', 'harga_beli', 'harga_jual')
        }),
    )


# === Inline Detail Pembelian ===
class DetailPembelianInline(admin.TabularInline):
    model = DetailPembelian
    extra = 1


# === Admin untuk Pembelian ===
@admin.register(Pembelian)
class PembelianAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'pemasok', 'total')
    search_fields = ('pemasok__nama',)
    list_filter = ('pemasok', 'tanggal')
    inlines = [DetailPembelianInline]
    readonly_fields = ('tanggal',)


# === Inline Detail Penjualan ===
class DetailPenjualanInline(admin.TabularInline):
    model = DetailPenjualan
    extra = 1


# === Admin untuk Penjualan ===
@admin.register(Penjualan)
class PenjualanAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'pelanggan', 'total', 'kasir')
    search_fields = ('pelanggan', 'kasir__username')
    list_filter = ('tanggal', 'kasir')
    inlines = [DetailPenjualanInline]
    readonly_fields = ('tanggal',)


# === Detail tidak perlu didaftarkan langsung karena ditangani via Inline ===
# Jika ingin tetap muncul di daftar admin, bisa register seperti ini:
# admin.site.register(DetailPembelian)
# admin.site.register(DetailPenjualan)