from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('request-success/<int:request_id>/', views.request_success, name='request_success'),
    path('track_order/', views.track_order, name='track_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)