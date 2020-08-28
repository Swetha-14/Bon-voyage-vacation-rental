from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("host", views.host, name="host"),
    path("place/<int:id>", views.place, name="place"),
    path("your_trips", views.trips, name="trips"),
    path("your_properties", views.properties, name="properties"),
    path("saved_properties", views.saved, name="saved"),
    path("place/<int:id>/payment", views.payment, name="payment"),
    path("edit/<int:id>", views.edit, name="edit")
]
