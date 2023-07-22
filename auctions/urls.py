from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create, name="create"),
    path('listing/<int:pk>', views.listing_detail_view, name='listing_detail'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove", views.remove_watchlist, name="remove_watchlist")
]
