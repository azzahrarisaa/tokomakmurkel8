from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.forms import inlineformset_factory
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('kasir', 'Kasir'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# Kategori Produk
class KategoriProduk(models.Model):
    nama = models.CharField(max_length=100, verbose_name=_("Nama Kategori"))
    deskripsi = models.TextField(blank=True, null=True, verbose_name=_("Deskripsi"))

    class Meta:
        verbose_name = _("Kategori Produk")
        verbose_name_plural = _("Kategori Produk")

    def __str__(self):
        return self.nama




# Satuan Produk
class Satuan(models.Model):
    nama = models.CharField(max_length=50, verbose_name=_("Nama Satuan"))

    class Meta:
        verbose_name = _("Satuan")
        verbose_name_plural = _("Satuan")

    def __str__(self):
        return self.nama


# Supplier
class Pemasok(models.Model):
    nama = models.CharField(max_length=100, verbose_name=_("Nama Pemasok"))
    kontak = models.CharField(max_length=100, verbose_name=_("Kontak"))
    alamat = models.TextField(verbose_name=_("Alamat"))

    class Meta:
        verbose_name = _("Pemasok")
        verbose_name_plural = _("Pemasok")

    def __str__(self):
        return self.nama


# Produk
class Produk(models.Model):
    kode_produk = models.CharField(max_length=20, unique=True, verbose_name=_("Kode Produk"))
    nama = models.CharField(max_length=200, verbose_name=_("Nama Produk"))
    kategori = models.ForeignKey(KategoriProduk, on_delete=models.SET_NULL, null=True, verbose_name=_("Kategori"))
    satuan = models.ForeignKey(Satuan, on_delete=models.SET_NULL, null=True, verbose_name=_("Satuan"))
    stok = models.PositiveIntegerField(default=0, verbose_name=_("Stok"))
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Harga Beli"))
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Harga Jual"))
    pemasok = models.ForeignKey(Pemasok, on_delete=models.SET_NULL, null=True, verbose_name=_("Pemasok"))
    gambar = models.ImageField(upload_to="produk/", null=True, blank=True, verbose_name=_("Foto Produk"))

    class Meta:
        verbose_name = _("Produk")
        verbose_name_plural = _("Produk")

    def __str__(self):
        return self.nama


# Transaksi Pembelian
class Pembelian(models.Model):
    tanggal = models.DateField(auto_now_add=True, verbose_name=_("Tanggal"))
    pemasok = models.ForeignKey(Pemasok, on_delete=models.CASCADE, verbose_name=_("Pemasok"))
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total"))

    class Meta:
        verbose_name = _("Pembelian")
        verbose_name_plural = _("Pembelian")

    def __str__(self):
        return f"{self.pemasok.nama} - {self.tanggal}"

class DetailPembelian(models.Model):
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE, related_name="detail_pembelian", verbose_name=_("Pembelian"))
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, verbose_name=_("Produk"))
    jumlah = models.PositiveIntegerField(verbose_name=_("Jumlah"))
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Harga Satuan"))

    class Meta:
        verbose_name = _("Detail Pembelian")
        verbose_name_plural = _("Detail Pembelian")

# Transaksi Penjualan
class Penjualan(models.Model):
    tanggal = models.DateField(auto_now_add=True, verbose_name=_("Tanggal"))
    pelanggan = models.CharField(max_length=100, verbose_name=_("Nama Pelanggan"))
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total"))
    kasir = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Kasir"))

    class Meta:
        verbose_name = _("Penjualan")
        verbose_name_plural = _("Penjualan")

    def __str__(self):
        return f"{self.pelanggan} - {self.tanggal}"


class DetailPenjualan(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE, related_name="detail_penjualan", verbose_name=_("Penjualan"))
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, verbose_name=_("Produk"))
    jumlah = models.PositiveIntegerField(verbose_name=_("Jumlah"))
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Harga Satuan"))

    class Meta:
        verbose_name = _("Detail Penjualan")
        verbose_name_plural = _("Detail Penjualan")