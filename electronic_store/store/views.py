import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .forms import *
from .models import *
from .utils import *
import folium

# Create your views here.


class IndexView(ListView):
    template_name = "store/index.html"
    context_object_name = "latest_items"

    def get_queryset(self):
        return Item.objects.order_by('item_cost')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_items'] = Item.objects.filter(num_of_views__gt=5)[:4]
        return context


def index(request):
    # return HttpResponse("<center><h2>Welcome page!</h2></center>")
    latest_items = Item.objects.order_by('-item_cost')
    return render(request, "store/index.html", {"latest_items": latest_items})


def get_item_by_id(request, id):
    item = get_object_or_404(Item, pk=id)
    return render(request, "store/item.html", {"item": item})
    # try:
    #     item = Item.objects.get(pk=id)
    #     return HttpResponse(f"<h3>{item.item_name} {item.item_desc}. Cost: {item.item_cost} tenge.</h3>")
    # except Exception as e:
    #     raise Http404(f"Oops! Error! {e}")


def search_item_by_name(request):
    if request.method == "POST" and len(request.POST.get("search_field")) > 0:
        searching_text = request.POST.get("search_field")
        return redirect("store:search_success", text=searching_text)
    else:
        return render(request, "store/search.html",
                      {"empty_res": "No results found"})


def search_success(request, text):
    if len(text) > 0:
        search_res = Item.objects.filter(item_name__contains=text)
        return render(request, "store/search.html", {"search_res": search_res, "empty_res": "No results found"})


def item_catalog(request):
    try:
        all_items = Item.objects.all()
        items = ""
        for it in all_items:
            items += f"<h3>Item ID # {it.id} - {it.item_name}" \
                     f" - {it.item_cost}</h3><br>"
            return HttpResponse(f"Results are:<br> {items}")
    except Exception as e:
        raise Http404(f"Oops! Error! {e}")


def departments(request):
    all_deps = Department.objects.order_by('dep_name')
    return render(request, "store/departments.html", {"all_deps": all_deps})


def get_dep_by_id(request, id):
    dep = get_object_or_404(Department, pk=id)
    items = list(Item.objects.filter(dep_id=dep.id))
    return render(request, "store/department.html", {"dep": dep, "items": items})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('store:index')
    else:
        # if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:index')
        else:
            messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store:login')


class ProfileView(TemplateView):
    template_name = "registration/user_page.html"


class registerView(CreateView):
    form_class = MyUserForm
    success_url = reverse_lazy('store:login')
    template_name = 'registration/register.html'


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # else:
        #     customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('Payment completed', safe=False)


def calculate_distance_view(request):
    distance = None
    obj = get_object_or_404(FindLocation, id=22)
    form = FindLocationModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='store')

    ips = [
        '217.196.24.37',
        '88.204.154.155',
        '188.0.129.134',
        '5.34.115.95'
    ]
    info = []
    for ip in ips:
        country, city, lat, long = get_geo(ip)
        info.append([country, city, lat, long])

    # city names
    locations = []
    for i in info:
        locations.append(geolocator.geocode(i[1]))

    points = []
    for i in info:
        points.append((i[2], i[3]))

    # initial folium map
    m = folium.Map(width=1125, height=700, location=get_center_coordinates(info[2][2], info[2][3], info[1][2], info[1][3]), zoom_start=5)

    # location markers
    folium.Marker([info[0][2], info[0][3]], tooltip='Nur-Sultan, Seifullin Street', popup=info[0][1]['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    folium.Marker([info[1][2], info[1][3]], tooltip='Almaty, Tole Bi Avenue', popup=info[1][1]['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    folium.Marker([info[2][2], info[2][3]], tooltip='Aktau, 16th Microdistrict', popup=info[2][1]['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    folium.Marker([info[3][2], info[3][3]], tooltip='Oral', popup=info[3][1]['city'],
                  icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        deliveryAddress_ = form.cleaned_data.get('deliveryAddress')
        deliveryAddress = geolocator.geocode(deliveryAddress_)

        # coordinates of delivery address
        d_lat = deliveryAddress.latitude
        d_long = deliveryAddress.longitude
        pointB = (d_lat, d_long)

        # calculating distances
        distances = []
        for p in points:
            distances.append(round(geodesic(p, pointB).km, 2))

        distance = min(distances)

        id = 0
        for d in distances:
            if distance == d:
                break
            else:
                id = id + 1

        # distance = round(geodesic(pointA, pointB).km, 2)

        m = folium.Map(width=1100, height=700, location=get_center_coordinates(info[2][2], info[2][3], info[1][2], info[1][3]),
                       zoom_start=get_zoom(distance))

        # location markers
        folium.Marker([info[0][2], info[0][3]], tooltip='Nur-Sultan', popup=info[0][1]['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        folium.Marker([info[1][2], info[1][3]], tooltip='Almaty', popup=info[1][1]['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        folium.Marker([info[2][2], info[2][3]], tooltip='Aktau', popup=info[2][1]['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        folium.Marker([info[3][2], info[3][3]], tooltip='Oral', popup=info[3][1]['city'],
                      icon=folium.Icon(color='purple')).add_to(m)

        # delivery address marker
        folium.Marker([d_lat, d_long], tooltip='click here for more', popup=deliveryAddress,
                      icon=folium.Icon(color='cloud')).add_to(m)

        # folium.Marker([l_lat, l_long], tooltip='click here for more', popup=city['city'],
        #               icon=folium.Icon(color='purple')).add_to(m)

        line = folium.PolyLine(locations=[points[id], pointB], weight=3, color='blue')
        m.add_child(line)

        instance.location = info[id][1]['city']
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'form': form,
        'map': m,
    }

    return render(request, 'store/map.html', context)
