from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *


# Create your views here.

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
        if request.method == 'POST':
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


class registerView(CreateView):
    form_class = MyUserForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
