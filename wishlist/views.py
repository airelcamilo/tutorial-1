from django.shortcuts import render
from wishlist.models import BarangWishlist
# Data delivery
from django.http import HttpResponse
from django.core import serializers
# Handle registrasi
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Handle login
from django.contrib.auth import authenticate, login
# Handle logout
from django.contrib.auth import logout
# Handle merestriksi akses halaman
from django.contrib.auth.decorators import login_required
# Handle cookies
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Menampilkan barang wishlist
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Airel Camilo Khairan',
        # Cookies
        'last_login': request.COOKIES['last_login']
    }
    return render(request, "wishlist.html", context)

# Menampilkan data berbentuk XML dan JSON
def show_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Menampilkan form registrasi
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

# Menampilkan form login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Cookies
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

# Handle logout di wishlist
def logout_user(request):
    logout(request)
    return redirect('wishlist:login')