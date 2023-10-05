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
    path('vocalizacion/', views.vocalizacion, name='vocalizacion'),
    path('vocalizacion/<int:pauta_id>/', views.vocalizacion, name='vocalizacion_con_pauta'),
    path('intensidad/<int:pauta_id>/', views.intensidad, name='intensidad_con_pauta'),
    path('intensidad/',views.intensidad, name="intensidad"),
    path('list_paci_admin/', views.list_paci_admin, name='list_paci_admin'), 
    path('list_fono_admin/', views.list_fono_admin, name='list_fono_admin'),
    path('list_neur_admin/', views.list_neur_admin, name='list_neur_admin'),
    path('list_fami_admin/', views.list_fami_admin, name='list_fami_admin'),
    path('listado_informes/', views.listado_informes, name='listado_informes'),
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
    path('ingresar_informes/', views.ingresar_informes, name='ingresar_informes'),
    path('editar_informe/<int:informe_id>/', views.editar_informe, name='editar_informe'),
    path('eliminar_informe/<int:informe_id>/', views.eliminar_informe, name='eliminar_informe'),
    path('eliminar_informe_admin/<int:informe_id>/', views.eliminar_informe_admin, name='eliminar_informe_admin'),
    path('detalle_informe/<int:informe_id>/', views.detalle_informe, name='detalle_informe'),
    path('detalle_prof_infor/<int:informe_id>/', views.detalle_prof_infor, name='detalle_prof_infor'),
    path('editar_informe_admin/<int:informe_id>/', views.editar_informe_admin, name='editar_informe_admin'),
    path('pacientes_disponibles/', views.pacientes_disponibles, name='pacientes_disponibles'),
    path('agregar_paciente/<int:paciente_id>/', views.agregar_paciente, name='agregar_paciente'),
    path('desvincular_paciente/<int:paciente_id>/', views.desvincular_paciente, name='desvincular_paciente'),
    path('detalle_prof_pauta/<int:id_pauta_terapeutica_id>/', views.detalle_prof_pauta, name='detalle_prof_pauta'),
    path('editar_prof_pauta/<int:id_pauta_terapeutica_id>/', views.editar_prof_pauta, name='editar_prof_pauta'),
    path('eliminar_prof_pauta/<int:id_pauta_terapeutica_id>/', views.eliminar_prof_pauta, name='eliminar_prof_pauta'),
    path('detalle_pauta_admin/<int:id_pauta_terapeutica_id>/', views.detalle_pauta_admin, name='detalle_pauta_admin'),
    path('editar_pauta_admin/<int:id_pauta_terapeutica_id>/', views.editar_pauta_admin, name='editar_pauta_admin'),
    path('eliminar_pauta_admin/<int:id_pauta_terapeutica_id>/', views.eliminar_pauta_admin, name='eliminar_pauta_admin'),
]

##urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
