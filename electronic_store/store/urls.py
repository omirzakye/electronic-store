from django.urls import path
from .views import *

app_name = "store"
urlpatterns = [
    path('', index, name="index"),
    path('item/<int:id>', get_item_by_id, name="get_item_by_id"),
    path('search/<str:text>', search_item_by_name, name="search_item_by_name"),
    path('catalog/', item_catalog, name="item_catalog"),
    path('departments/', departments, name="departments"),
    path('department/<int:id>', get_dep_by_id, name="get_dep_by_id"),
    path('search/', search_item_by_name, name='search_item_by_name'),
    path('search/<str:text>/', search_success, name='search_success')
]
