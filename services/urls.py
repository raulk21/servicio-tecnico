from django.urls import path
from . import views
from .views import check_order
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),

    # cliente
    path("track-order/", views.track_order, name="track_order"),
    path("panel/", views.client_panel, name="client_panel"),
    path("orden/<str:order_number>/", views.order_detail, name="order_detail"),

    # taller
    path("panel-taller/", views.workshop_panel, name="workshop_panel"),
    path("order/<int:order_id>/", views.update_order, name="update_order"),

    path(
        "update-order/<int:order_id>/<str:new_status>/",
        views.update_order_status,
        name="update_order_status"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)