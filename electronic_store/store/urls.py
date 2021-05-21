from django.urls import path
from .views import *

app_name = "store"
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('item/<int:id>', get_item_by_id, name="get_item_by_id"),
    path('search/<str:text>', search_item_by_name, name="search_item_by_name"),
    path('catalog/', item_catalog, name="item_catalog"),
    path('departments/', departments, name="departments"),
    path('department/<int:id>', get_dep_by_id, name="get_dep_by_id"),
    path('search/', search_item_by_name, name='search_item_by_name'),
    path('search/<str:text>/', search_success, name='search_success'),
    path('user_page/<int:id>/', ProfileView.as_view(), name='user_page'),
    path('login/', loginUser, name="login"),
    path('register/', registerView.as_view(), name="registration"),
    path('logout/', logoutUser, name="logout"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    path('map/', calculate_distance_view, name="map"),
]
