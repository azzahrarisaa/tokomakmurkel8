from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from math import ceil
import uuid

from .models import (
    Produk,
    KategoriProduk,
    Satuan,
    Pemasok,
    Pembelian,
    DetailPembelian,
    Penjualan,
    DetailPenjualan,
    Profile,
)

#BERANDA
def beranda(request):
    total_produk = Produk.objects.count()
    total_stok = sum(p.stok for p in Produk.objects.all())
    total_penjualan = Penjualan.objects.count()
    total_pembelian = Pembelian.objects.count()

    context = {
        'total_produk': total_produk,
        'total_stok': total_stok,
        'total_penjualan': total_penjualan,
        'total_pembelian': total_pembelian,
    }
    return render(request, 'beranda.html', context)

#DASHBOARD
def dashboard(request):
    total_produk = Produk.objects.count()
    total_stok = Produk.objects.aggregate(total=Sum('stok'))['total'] or 0
    total_penjualan = Penjualan.objects.aggregate(total=Sum('total'))['total'] or 0
    total_pembelian = Pembelian.objects.aggregate(total=Sum('total'))['total'] or 0

   # Skala grafik: ubah ke ribuan
    penjualan_rb = total_penjualan / 1000
    pembelian_rb = total_pembelian / 1000

    max_chart = max(total_produk, total_stok, penjualan_rb, pembelian_rb)
    max_chart = ceil(max_chart / 500) * 500  

    context = {
        'total_produk': total_produk,
        'total_stok': total_stok,
        'total_penjualan': total_penjualan,
        'total_pembelian': total_pembelian,
        'penjualan_rb': penjualan_rb,
        'pembelian_rb': pembelian_rb,
        'max_chart': max_chart
    }

    return render(request, 'produk/dashboard.html', context)

#USER
def daftar_user(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'produk/user.html', {'users': users})

def tambah_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True if role == 'admin' else False
        user.save()

        user.profile.role = role
        user.profile.save()

        messages.success(request, 'User berhasil ditambahkan.')
        return redirect('daftar_user')

    return render(request, 'produk/tambah_user.html')

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, created = Profile.objects.get_or_create(user=user)  # ⬅ ini yang kamu ubah

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        role = request.POST['role']

        user.username = username
        user.email = email
        user.is_staff = True if role == 'admin' else False

        password = request.POST.get('password', '')
        if password:
            user.set_password(password)
        user.save()

        profile.role = role
        profile.save()

        messages.success(request, 'User berhasil diupdate.')
        return redirect('daftar_user')

    return render(request, 'produk/edit_user.html', {'user': user, 'profile': profile})

def hapus_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User berhasil dihapus.')
        return redirect('daftar_user')

    # Bisa buat konfirmasi hapus, atau langsung hapus tanpa konfirmasi kalau mau
    return render(request, 'produk/konfirmasi_hapus_user.html', {'user': user})

#PRODUK
def produk(request):
    if request.method == 'POST':
        # Ambil data dari form
        kode_produk = request.POST['kode_produk']
        nama = request.POST['nama']
        kategori = KategoriProduk.objects.get(id=request.POST['kategori'])
        satuan = Satuan.objects.get(id=request.POST['satuan'])
        stok = request.POST['stok']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']
        pemasok = Pemasok.objects.get(id=request.POST['pemasok'])
        gambar = request.FILES.get('gambar')

        # Simpan produk
        Produk.objects.create(
            kode_produk=kode_produk,
            nama=nama,
            kategori=kategori,
            satuan=satuan,
            stok=stok,
            harga_beli=harga_beli,
            harga_jual=harga_jual,
            pemasok=pemasok,
            gambar=gambar
        )
        return redirect('produk')  # atau redirect ke 'daftar_produk'

    # GET request - tampilkan form dan tabel
    produk = Produk.objects.all()
    kategori = KategoriProduk.objects.all()
    satuan = Satuan.objects.all()
    pemasok = Pemasok.objects.all()

    return render(request, 'produk/produk.html', {
    'produk': produk,
    'kategori': kategori,
    'satuan': satuan,
    'pemasok': pemasok,
})

def tambah_produk(request):
    kategori_list = KategoriProduk.objects.all()
    satuan = Satuan.objects.all()
    pemasok = Pemasok.objects.all()

    if request.method == 'POST':
        Produk.objects.create(
            kode_produk=request.POST['kode_produk'],
            nama=request.POST['nama'],
            kategori_id=request.POST['kategori'],
            satuan_id=request.POST['satuan'],
            stok=request.POST['stok'],
            harga_beli=request.POST['harga_beli'],
            harga_jual=request.POST['harga_jual'],
            pemasok_id=request.POST['pemasok'],
            gambar=request.FILES.get('gambar')
        )
        return redirect('daftar_produk')

    return render(request, 'produk/tambah_produk.html', {
        'kategori_list': kategori_list,
        'satuan': satuan,
        'pemasok': pemasok,
    })
    
def daftar_produk(request):
    produk = Produk.objects.all()
    return render(request, 'produk/daftar_produk.html', {'produk': produk})

def edit_produk(request, id):
    produk = Produk.objects.get(pk=id)
    kategori = KategoriProduk.objects.all()
    satuan = Satuan.objects.all()
    pemasok = Pemasok.objects.all()

    if request.method == 'POST':
        produk.kode_produk = request.POST['kode_produk']
        produk.nama = request.POST['nama']
        produk.kategori_id = request.POST['kategori']
        produk.satuan_id = request.POST['satuan']
        produk.stok = request.POST['stok']
        produk.harga_beli = request.POST['harga_beli']
        produk.harga_jual = request.POST['harga_jual']
        produk.pemasok_id = request.POST['pemasok']
        if 'gambar' in request.FILES:
            produk.gambar = request.FILES['gambar']
        produk.save()
        return redirect('daftar_produk')

    return render(request, 'produk/edit_produk.html', {
        'produk': produk,
        'kategori_list': kategori,
        'satuan': satuan,
        'pemasok': pemasok,
    })

def hapus_produk(request, id):
    produk = Produk.objects.get(pk=id)
    produk.delete()
    return redirect('daftar_produk')

#KATEGORI
def kategori_produk(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        KategoriProduk.objects.create(nama=nama, deskripsi=deskripsi)
        return redirect('kategori_produk')

    data = KategoriProduk.objects.all()
    return render(request, 'produk/kategori.html', {'data': data})

def tambah_kategori(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        deskripsi = request.POST.get('deskripsi', '')
        KategoriProduk.objects.create(nama=nama, deskripsi=deskripsi)
        return redirect('kategori_produk')
    return render(request, 'produk/tambah_kategori.html')

def edit_kategori(request, id):
    kategori = get_object_or_404(KategoriProduk, id=id)
    if request.method == 'POST':
        kategori.nama = request.POST['nama']
        kategori.deskripsi = request.POST.get('deskripsi', '')
        kategori.save()
        return redirect('kategori_produk')  # ✅ Fixed here
    return render(request, 'produk/edit_kategori.html', {'kategori': kategori})

def hapus_kategori(request, id):
    kategori = get_object_or_404(KategoriProduk, id=id)
    kategori.delete()
    return redirect('kategori_produk')

#SATUAN
def satuan_produk(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            Satuan.objects.create(nama=nama)
            messages.success(request, 'Satuan berhasil ditambahkan.')
            return redirect('satuan_produk')

    data = Satuan.objects.all()
    return render(request, 'produk/satuan.html', {'data': data})

def tambah_satuan(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        Satuan.objects.create(nama=nama)
        messages.success(request, 'Satuan berhasil ditambahkan.')
        return redirect('satuan_produk')
    
    # ✅ Perbaikan di sini
    return render(request, 'produk/tambah_satuan.html')


def edit_satuan(request, id):
    satuan = get_object_or_404(Satuan, id=id)
    if request.method == 'POST':
        satuan.nama = request.POST['nama']
        satuan.save()
        messages.success(request, 'Satuan berhasil diperbarui.')
        return redirect('satuan_produk')
    return render(request, 'produk/edit_satuan.html', {'satuan': satuan})


def hapus_satuan(request, id):
    satuan = get_object_or_404(Satuan, id=id)
    satuan.delete()
    messages.success(request, 'Satuan berhasil dihapus.')
    return redirect('satuan_produk')

#PEMASOK
def daftar_pemasok(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        alamat = request.POST.get('alamat')
        Pemasok.objects.create(nama=nama, kontak=kontak, alamat=alamat)
        return redirect('pemasok')

    data = Pemasok.objects.all()
    return render(request, 'produk/pemasok.html', {'data': data})

def tambah_pemasok(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        kontak = request.POST['kontak']
        alamat = request.POST['alamat']
        Pemasok.objects.create(nama=nama, kontak=kontak, alamat=alamat)
        return redirect('pemasok')
    return render(request, 'produk/tambah_pemasok.html')

def edit_pemasok(request, id):
    pemasok = get_object_or_404(Pemasok, pk=id)
    if request.method == 'POST':
        pemasok.nama = request.POST['nama']
        pemasok.kontak = request.POST['kontak']
        pemasok.alamat = request.POST['alamat']
        pemasok.save()
        return redirect('pemasok')
    return render(request, 'produk/edit_pemasok.html', {'pemasok': pemasok})

def hapus_pemasok(request, id):
    pemasok = get_object_or_404(Pemasok, pk=id)
    pemasok.delete()
    return redirect('pemasok')

#PENJUALAN
def daftar_penjualan(request):
    if request.method == 'POST':
        pelanggan = request.POST.get('pelanggan')
        total = request.POST.get('total')
        kasir_id = request.POST.get('kasir')

        if pelanggan and total and kasir_id:
            Penjualan.objects.create(
                pelanggan=pelanggan,
                total=total,
                kasir_id=kasir_id  # karena ini FK, pakai ID
            )
            return redirect('penjualan')

    data = Penjualan.objects.all().order_by('-tanggal')
    kasir_list = User.objects.all()
    return render(request, 'produk/penjualan.html', {'data': data, 'kasir_list': kasir_list})


def edit_penjualan(request, id):
    penjualan = get_object_or_404(Penjualan, id=id)
    detail_penjualan = DetailPenjualan.objects.filter(penjualan=penjualan)
    kasir_list = User.objects.all()
    produk_list = Produk.objects.all()

    if request.method == 'POST':
        pelanggan = request.POST.get('pelanggan')
        kasir_id = request.POST.get('kasir')
        produk_ids = request.POST.getlist('produk_id[]')
        jumlahs = request.POST.getlist('jumlah[]')
        harga_satuans = request.POST.getlist('harga_satuan[]')

        total = 0
        detail_items = []

        for i in range(len(produk_ids)):
            try:
                produk = Produk.objects.get(id=produk_ids[i])
                jumlah = int(jumlahs[i])
                harga_satuan = float(harga_satuans[i])
                subtotal = jumlah * harga_satuan
                total += subtotal

                detail_items.append({
                    'produk': produk,
                    'jumlah': jumlah,
                    'harga_satuan': harga_satuan
                })
            except:
                continue

        penjualan.pelanggan = pelanggan
        penjualan.kasir = User.objects.get(id=kasir_id)
        penjualan.total = total
        penjualan.save()

        # Hapus semua detail lama, lalu masukkan yang baru
        penjualan.detail_penjualan.all().delete()
        for item in detail_items:
            DetailPenjualan.objects.create(
                penjualan=penjualan,
                produk=item['produk'],
                jumlah=item['jumlah'],
                harga_satuan=item['harga_satuan']
            )

        return redirect('penjualan')

    return render(request, 'produk/edit_penjualan.html', {
        'penjualan': penjualan,
        'detail_penjualan': detail_penjualan,
        'kasir_list': kasir_list,
        'produk_list': produk_list
    })

def detail_penjualan(request, id):
    penjualan = get_object_or_404(Penjualan, id=id)
    detail = DetailPenjualan.objects.filter(penjualan=penjualan)
    return render(request, 'produk/detail_penjualan.html', {
        'penjualan': penjualan,
        'detail': detail
    })

def tambah_penjualan(request):
    if request.method == 'POST':
        pelanggan = request.POST['pelanggan']
        kasir_id = request.POST['kasir']
        produk_ids = request.POST.getlist('produk_id[]')
        jumlah_list = request.POST.getlist('jumlah[]')
        harga_list = request.POST.getlist('harga_satuan[]')

        kasir = get_object_or_404(User, id=kasir_id)
        total = sum(float(j) * float(h) for j, h in zip(jumlah_list, harga_list))

        # Buat objek Penjualan
        penjualan = Penjualan.objects.create(
            pelanggan=pelanggan,
            total=total,
            kasir=kasir
        )

        for produk_id, jumlah, harga_satuan in zip(produk_ids, jumlah_list, harga_list):
            produk = get_object_or_404(Produk, id=produk_id)

            # Cek stok cukup
            if produk.stok < int(jumlah):
                messages.error(request, f"Stok produk '{produk.nama}' tidak cukup.")
                return redirect('tambah_penjualan')

            # Simpan DetailPenjualan
            DetailPenjualan.objects.create(
                penjualan=penjualan,
                produk=produk,
                jumlah=jumlah,
                harga_satuan=harga_satuan
            )

            # Kurangi stok produk
            produk.stok -= int(jumlah)
            produk.save()

        messages.success(request, 'Penjualan berhasil ditambahkan.')
        return redirect('penjualan')

    # GET method: tampilkan form
    kasir_list = User.objects.all()
    produk_list = Produk.objects.all()
    return render(request, 'produk/tambah_penjualan.html', {
        'kasir_list': kasir_list,
        'produk_list': produk_list,
    })

def hapus_penjualan(request, id):
    penjualan = get_object_or_404(Penjualan, id=id)
    penjualan.delete()
    return redirect('penjualan')

#PEMBELIAN
def daftar_pembelian(request):
    if request.method == 'POST':
        pemasok_id = request.POST.get('pemasok_id')
        total = request.POST.get('total')
        if pemasok_id and total:
            Pembelian.objects.create(
                pemasok_id=pemasok_id,
                total=total
            )
            return redirect('pembelian')

    data = Pembelian.objects.order_by('id')
    pemasok = Pemasok.objects.all()
    return render(request, 'produk/pembelian.html', {'data': data, 'pemasok': pemasok})

def tambah_pembelian(request):
    if request.method == 'POST':
        pemasok_id = request.POST.get('pemasok_id')
        produk_ids = request.POST.getlist('produk_id[]')  # produk lama
        nama_produk_list = request.POST.getlist('nama_produk_baru[]')  # produk baru
        kode_produk_list = request.POST.getlist('kode_produk_baru[]')
        harga_beli_baru = request.POST.getlist('harga_beli_baru[]')
        harga_jual_baru = request.POST.getlist('harga_jual_baru[]')
        jumlah_list = request.POST.getlist('jumlah[]')
        harga_list = request.POST.getlist('harga_satuan[]')

        if not pemasok_id:
            messages.error(request, 'Pemasok harus dipilih.')
            return redirect('tambah_pembelian')

        pemasok = get_object_or_404(Pemasok, id=pemasok_id)
        total = 0

        pembelian = Pembelian.objects.create(
            pemasok=pemasok,
            total=0  # sementara
        )

        index = 0

        # 1. Tambahkan produk baru jika ada
        for i in range(len(nama_produk_list)):
            if nama_produk_list[i].strip() == "":
                continue  # skip kalau kosong

            produk_baru = Produk.objects.create(
                nama=nama_produk_list[i],
                kode_produk=kode_produk_list[i],
                harga_beli=harga_beli_baru[i],
                harga_jual=harga_jual_baru[i],
                pemasok=pemasok,
                stok=0
            )

            jumlah = int(jumlah_list[index])
            harga_satuan = float(harga_list[index])

            DetailPembelian.objects.create(
                pembelian=pembelian,
                produk=produk_baru,
                jumlah=jumlah,
                harga_satuan=harga_satuan
            )

            produk_baru.stok += jumlah
            produk_baru.save()

            total += jumlah * harga_satuan
            index += 1

        # 2. Tambahkan produk lama jika ada
        for i in range(len(produk_ids)):
            if not produk_ids[i]:
                continue

            produk = get_object_or_404(Produk, id=produk_ids[i])
            jumlah = int(jumlah_list[index])
            harga_satuan = float(harga_list[index])

            DetailPembelian.objects.create(
                pembelian=pembelian,
                produk=produk,
                jumlah=jumlah,
                harga_satuan=harga_satuan
            )

            produk.stok += jumlah
            produk.save()

            total += jumlah * harga_satuan
            index += 1

        pembelian.total = total
        pembelian.save()

        messages.success(request, 'Pembelian berhasil disimpan.')
        return redirect('daftar_pembelian')

    pemasok = Pemasok.objects.all()
    produk_list = Produk.objects.order_by('id')  # <-- ini bagian penting
    return render(request, 'produk/tambah_pembelian.html', {
    'pemasok': pemasok,
    'produk_list': produk_list,
})


def detail_pembelian(request, id):
    pembelian = get_object_or_404(Pembelian, id=id)
    detail = pembelian.detail_pembelian.all()  # related_name dari model DetailPembelian
    return render(request, 'produk/detail_pembelian.html', {
        'pembelian': pembelian,
        'detail': detail,
    })

def edit_pembelian(request, id):
    pembelian = get_object_or_404(Pembelian, id=id)

    if request.method == 'POST':
        pemasok_id = request.POST.get('pemasok_id')
        produk_ids = request.POST.getlist('produk_id[]')
        jumlah_list = request.POST.getlist('jumlah[]')
        harga_list = request.POST.getlist('harga_satuan[]')

        pemasok = get_object_or_404(Pemasok, id=pemasok_id)
        pembelian.pemasok = pemasok
        pembelian.total = sum(
            float(jml) * float(hrg)
            for jml, hrg in zip(jumlah_list, harga_list)
        )
        pembelian.save()

        # Hapus detail lama, simpan ulang
        pembelian.detail_pembelian.all().delete()

        for produk_id, jumlah, harga_satuan in zip(produk_ids, jumlah_list, harga_list):
            produk = get_object_or_404(Produk, id=produk_id)
            DetailPembelian.objects.create(
                pembelian=pembelian,
                produk=produk,
                jumlah=jumlah,
                harga_satuan=harga_satuan
            )

            # Update stok
            produk.stok += int(jumlah)
            produk.save()

        messages.success(request, 'Pembelian berhasil diperbarui.')
        return redirect('daftar_pembelian')

    pemasok = Pemasok.objects.all()
    produk_list = Produk.objects.all()
    detail_pembelian = pembelian.detail_pembelian.all()  # ✅ pakai related_name

    return render(request, 'produk/edit_pembelian.html', {
        'pembelian': pembelian,
        'pemasok': pemasok,
        'produk_list': produk_list,
        'detail_pembelian': detail_pembelian,
    })

def hapus_pembelian(request, id):
    pembelian = get_object_or_404(Pembelian, id=id)
    pembelian.delete()
    messages.success(request, 'Pembelian berhasil dihapus.')
    return redirect('daftar_pembelian')