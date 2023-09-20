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
    path('list_paci_admin/', views.list_paci_admin, name='list_paci_admin'), 
    path('list_fono_admin/', views.list_fono_admin, name='list_fono_admin'),
    path('list_neur_admin/', views.list_neur_admin, name='list_neur_admin'),
    path('list_fami_admin/', views.list_fami_admin, name='list_fami_admin'),
    path('detalle_paciente/<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('detalle_fonoaudiologo/<int:fonoaudiologo_id>/', views.detalle_fonoaudiologo, name='detalle_fonoaudiologo'),
    path('detalle_neurologo/<int:neurologo_id>/', views.detalle_neurologo, name='detalle_neurologo'),
    path('detalle_familiar_admin/<int:familiar_id>/', views.detalle_familiar_admin, name='detalle_familiar_admin'),
    path('lista_familiar/', views.lista_familiar, name='lista_familiar'),
    path('detalle_prof_paci/<int:paciente_id>/', views.detalle_prof_paci, name='detalle_prof_paci'),
    path('detalle_familiar/<int:paciente_id>/', views.detalle_familiar, name='detalle_familiar'),
    path('mi_fonoaudiologo/',views.mi_fonoaudiologo,name='mi_fonoaudiologo'),
    path('obtener_provincias/', views.obtener_provincias, name='obtener_provincias'),
    path('obtener_comunas/', views.obtener_comunas, name='obtener_comunas'),
]

##urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
