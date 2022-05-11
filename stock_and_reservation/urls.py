from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.overview, name="overview"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("registration", views.registration, name="registration"),
    path("registration_succeed", views.registration_succeed, name="registration_succeed"),
    path("logout", views.log_out, name="log_out"),
    path("stock", views.stock, name="stock"),
    path('make_reservation', views.make_reservation, name='make_reservation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
