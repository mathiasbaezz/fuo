from django.contrib import admin
from .models import *
# Register your models here.

class EventoPartidoUncaInline(admin.TabularInline):
    model = EventoPartidoUnca
    extra = 1

class EventosUncaInline(admin.TabularInline):
    model = EventosUnca
    extra = 1

class PartidoUncaAdmin(admin.ModelAdmin):
    list_display = ('equipo_local', 'equipo_visitante', 'goles_local', 'goles_visitante', 'penales_local', 'penales_visitante', 'fecha', 'fase_partido', 'deporte')
    inlines = [EventoPartidoUncaInline, EventosUncaInline]
    list_filter = ('fase_partido', 'deporte')
    search_fields = ('equipo_local__nombre', 'equipo_visitante__nombre', 'fase_partido')

class EquipoUncaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen')

class EventosUncaAdmin(admin.ModelAdmin):
    list_display = ('partido', 'minuto', 'tipo', 'jugadores')

class TablaPosicionesAdmin(admin.ModelAdmin):
    list_display = ('deporte', 'equipo', 'puesto', 'puntos')
    search_fields = ('equipo__nombre', 'deporte')
    list_filter = ('deporte', 'puesto')

admin.site.register(TablaPosiciones, TablaPosicionesAdmin)
admin.site.register(PartidoUnca, PartidoUncaAdmin)
admin.site.register(EquipoUnca, EquipoUncaAdmin)
admin.site.register(EventosUnca, EventosUncaAdmin)
admin.site.register(EventoPartidoUnca)
admin.site.register(CampeonUnca)
admin.site.register(DeporteUnca)
admin.site.register(ChampionUnca)
admin.site.register(ChampiongralUnca)
admin.site.register(Categoria1)
admin.site.register(Categoria2)
admin.site.register(Categoria3)
admin.site.register(Post)
admin.site.register(AtletismoFeso)


