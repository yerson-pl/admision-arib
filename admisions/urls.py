from django.urls import path

from . import views



app_name = 'admisions'
urlpatterns = [
    path('', view=views.AdmisionHomeView.as_view(), name='index'),
    #path('inscripcion/', view=views.AdmisionInscripcionView.as_view(), name='inscripcion'),
    path('inscripcion/', views.crearPostulante , name='inscripcion'),
    path('ficha/', view =views.ReporteInscripcionPdf.as_view(), name='ficha'),
    path('confirmacion/', view=views.ConfirmacionView.as_view(), name='confirmacion'),
    path('email/', view=views.Email.as_view(), name="email"),
    #path('ficha2/', views.hello, name='ficha2'),
    #path('registrarPostulante/', views.crearPostulante)
    path('postulantes/list', views.listar, name='postulante_list'),
    #reportes
    path('postulantes/print', views.postulante_print, name='postulante_print'),
    path('postulantes/print/<int:pk>', views.postulante_print, name='postulante_print_one'),
    path('postulantes/grafico', views.grafico, name='postulante_grafico')  

]