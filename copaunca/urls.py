"""cpingfolder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cpunca import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admnfuo24/', admin.site.urls),
    path('', views.raiz),
    path('tabla_posiciones_fuo/', views.actualizar_tabla_posiciones, name='tabla_posiciones'),
    path('resultados_fuo/', views.mostrar_partidos_unca, name='partidos'),
    path('resultados_fuo/<int:pk>/', views.resumen_unca, name='resumen'),
    path('fuo/', views.deportes_unca),
    path('campeones_fuo/', views.tabla_campeones_unca),
    path('atletismo/', views.mostrar_atlestismo_feso),
    path('tabla_atletismo/', views.tabla_posiciones_atletismo, name='tabla_posiciones'),
    path ('noticias', views.blog),
    path ('noticias/<slug:pk>', views.single_blog, name='single_blog'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


