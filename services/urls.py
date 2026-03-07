from django.urls import path
from . import views
from .views import check_order
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('request-success/<int:request_id>/', views.request_success, name='request_success'),
    path('track_order/', views.track_order, name='track_order'),
    path('check-order/', check_order, name='check_order'),
    path('panel/', views.client_panel, name='client_panel'),
    path("orden/<str:order_number>/", views.order_detail, name="order_detail"),
    path("update-order/<int:order_id>/<str:new_status>/",
    views.update_order_status,
    name="update_order_status"),
    path("panel-taller/", views.workshop_panel, name="workshop_panel"),
    #path("order/<str:order_number>/", views.order_detail, name="order_detail"),
    path("order/<int:order_id>/", views.update_order, name="update_order"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)