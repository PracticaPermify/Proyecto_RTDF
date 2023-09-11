from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login_view, name="login"),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'), 
    path('listado_pacientes/', views.listado_pacientes, name='listado_pacientes'),
    path('vocalizacion/',views.vocalizacion, name="vocalizacion"),
    path('intensidad/',views.intensidad, name="intensidad"),
]

##urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
