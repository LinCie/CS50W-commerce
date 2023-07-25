from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    
    path("listing/new/", views.create, name="create"),
    path("listing/<int:pk>/edit/", views.edit, name="edit"),
    path("listing/<int:pk>/", views.listing_detail_view, name="listing_detail"),
    
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove", views.remove_watchlist, name="remove_watchlist"),
    
    path("category/", views.category, name="category"),
    path("category/<str:slug>/", views.category_view, name='category_view'),
    path("category/add", views.add_category, name="add_category"),
    path("category/get/<int:pk>", views.get_category, name="get_category"),
    
    path("bid/<int:pk>/", views.bid, name="bid"),
    path("bid/<int:pk>/get", views.get_bid, name="get_bid")
]
