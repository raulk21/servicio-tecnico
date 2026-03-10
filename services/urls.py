from django.urls import path
from . import views
from .views import check_order


urlpatterns = [
    path("", views.home, name="home"),
    path('servicio/<int:service_id>/', views.service_detail, name='service_detail'),

    # cliente
    path("seguimiento-orden/", views.track_order, name="track_order"),
    path("panel/", views.client_panel, name="client_panel"),
    path("orden/<str:order_number>/", views.order_detail, name="order_detail"),

    # taller
    path("taller/panel", views.workshop_panel, name="workshop_panel"),
    path("orden/<int:order_id>/", views.update_order, name="update_order"),

    path(
        "actualizar-orden/<int:order_id>/<str:new_status>/",
        views.update_order_status,
        name="update_order_status"
    ),
    path("solicitar-reparacion/", views.request_repair, name="request_repair"),
    path("solicitud-enviada/<int:request_id>", views.request_success, name="request_success"),
]