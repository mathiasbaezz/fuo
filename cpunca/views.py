
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import random
from django.core.paginator import Paginator

def index(request):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    return render(request, 'fuo.html', {'posts':posts})

def raiz(request):
    return redirect('/fuo')




def tabla_campeones_unca(request):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    equipos = EquipoUnca.objects.all()
    champions = ChampionUnca.objects.all()

    # Crear o actualizar las posiciones para cada equipo
    for equipo in equipos:
        campeon, created = CampeonUnca.objects.get_or_create(equipo=equipo)
        # Calcula los puntos totales para cada deporte y género
        total_campeonatos = (
            campeon.campeon_2016 +
            campeon.campeon_2017 +
            campeon.campeon_2018 +
            campeon.campeon_2019 +
            campeon.campeon_2022 +
            campeon.campeon_2023
        )
        # Actualiza los puntos en la posición del equipo
        campeon.total_campeonatos = total_campeonatos
        campeon.save()

    # Obtén todas las posiciones ordenadas por puntaje total (de mayor a menor)
    campeones = CampeonUnca.objects.order_by('-total_campeonatos')

    return render(request, 'tabla_campeonesfuo.html', {'posts':posts, 'campeones': campeones, 'champions': champions})

def mostrar_partidos_unca(request):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    deporte = request.GET.get('deporte', 'FUTBOL_FEMENINO')  # Valor por defecto: Fútbol Masculino
    partidos = PartidoUnca.objects.filter(deporte=deporte).order_by('-id')
    return render(request, 'partidosfuo.html', {'partidouncas': partidos, 'posts':posts})


def mostrar_atlestismo_feso(request):
    posts = Post.objects.all().order_by('-published_date')[:4]
    deporte = request.GET.get('deporte', '100M_FEMENINO')
    atletismofesos = AtletismoFeso.objects.filter(deporte=deporte).order_by('-id')
    return render(request, '100m.html', {'atletismofesos': atletismofesos, 'posts': posts})




def resumen_unca(request, pk):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    partido = get_object_or_404(PartidoUnca, pk=pk)
    partidos = PartidoUnca.objects.all()
    eventos_partido = EventoPartidoUnca.objects.filter(partido=partido)
    eventos = EventosUnca.objects.filter(partido=partido)

    context = {
        'partidounca': partido,
        'partidos': partidos,
        'eventos_partido': eventos_partido,
        'eventos': eventos,
        'posts': posts
    }

    return render(request, 'resumenfuo.html', context)


def deportes_unca (request):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    deportes = DeporteUnca.objects.all()
    return render(request, 'fuo.html', {"posts": posts, "deportes":deportes})


def champions_unca (request):
    posts = Post.objects.all().order_by('-published_date')[0:4]
    champions = ChampionUnca.objects.all()
    championsgral = ChampiongralUnca.objects.all()
    return render(request, 'tabla_campeonesfuo.html', {'posts':posts, "champions":champions, "championsgral":championsgral})







def blog (request):
    posts = Post.objects.all().order_by('-published_date')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    paginator_posts = paginator.get_page(page)
    posts = Post.objects.all().order_by('-published_date')[0:6]
    contexto = {"posts_pagin": paginator_posts, "posts": posts}
    return render(request, 'blog.html', contexto)

def single_blog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    posts = Post.objects.all().order_by('-published_date')[0:6]
    contexto = {"post": post, "posts":posts}
    return render(request, 'single_blog.html', contexto)


def tabla_posiciones_atletismo(request):
    # Inicializamos un diccionario para almacenar las puntuaciones por equipo y deporte
    puntuaciones = {}

    # Obtenemos todas las competiciones
    competencias = AtletismoFeso.objects.all()

    for competencia in competencias:
        # Para el primer puesto
        if competencia.primer_puesto:
            if competencia.primer_puesto not in puntuaciones:
                puntuaciones[competencia.primer_puesto] = []
            puntuaciones[competencia.primer_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 10,
                'emoji': '🥇'
            })

        # Para el segundo puesto
        if competencia.segundo_puesto:
            if competencia.segundo_puesto not in puntuaciones:
                puntuaciones[competencia.segundo_puesto] = []
            puntuaciones[competencia.segundo_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 6,
                'emoji': '🥈'
            })

        # Para el tercer puesto
        if competencia.tercer_puesto:
            if competencia.tercer_puesto not in puntuaciones:
                puntuaciones[competencia.tercer_puesto] = []
            puntuaciones[competencia.tercer_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 4,
                'emoji': '🥉'
            })

        # Para el cuarto puesto
        if competencia.cuarto_puesto:
            if competencia.cuarto_puesto not in puntuaciones:
                puntuaciones[competencia.cuarto_puesto] = []
            puntuaciones[competencia.cuarto_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 3,
                'emoji': '4️⃣'
            })

        # Para el quinto puesto
        if competencia.quinto_puesto:
            if competencia.quinto_puesto not in puntuaciones:
                puntuaciones[competencia.quinto_puesto] = []
            puntuaciones[competencia.quinto_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 2,
                'emoji': '5️⃣'
            })

        # Para el sexto puesto
        if competencia.sexto_puesto:
            if competencia.sexto_puesto not in puntuaciones:
                puntuaciones[competencia.sexto_puesto] = []
            puntuaciones[competencia.sexto_puesto].append({
                'deporte': competencia.get_deporte_display,
                'puntos': 1,
                'emoji': '6️⃣'
            })

    # Convertimos las puntuaciones en una lista con la suma total de puntos por equipo y el detalle de los deportes
    posiciones_ordenadas = []
    for equipo, resultados in puntuaciones.items():
        total_puntos = sum([r['puntos'] for r in resultados])
        posiciones_ordenadas.append({
            'equipo': equipo,
            'puntos': total_puntos,
            'detalles': resultados  # Almacenamos los detalles del deporte y puntos
        })

    # Ordenamos los equipos por su puntuación total
    posiciones_ordenadas.sort(key=lambda x: x['puntos'], reverse=True)

    return render(request, 'tabla_atletismo.html', {'posiciones_ordenadas': posiciones_ordenadas})


from django.db.models import Q


from django.db.models import Sum


def actualizar_tabla_posiciones(request):
    equipos = {}
    deportes_claves = dict(PartidoUnca.DEPORTE_CHOICES)  # Crear un diccionario para fácil búsqueda de nombres legibles

    for deporte_clave in deportes_claves.keys():
        semifinales = PartidoUnca.objects.filter(fase_partido='Semifinal', deporte=deporte_clave)
        final = PartidoUnca.objects.filter(fase_partido='Final', deporte=deporte_clave).first()

        if final is None:
            continue

        if final.goles_local > final.goles_visitante or (
                final.goles_local == final.goles_visitante and final.penales_local > final.penales_visitante):
            primer_puesto = final.equipo_local
            segundo_puesto = final.equipo_visitante
        else:
            primer_puesto = final.equipo_visitante
            segundo_puesto = final.equipo_local

        if semifinales.exists():
            tercer_puesto, cuarto_puesto = TercerPuestoLogica.determinar_tercer_puesto(semifinales)
        else:
            tercer_puesto, cuarto_puesto = None, None

        puntos_por_posicion = {1: 10, 2: 6, 3: 4, 4: 3}

        # Actualizar tabla de posiciones
        TablaPosiciones.objects.update_or_create(
            deporte=deporte_clave, equipo=primer_puesto,
            defaults={'puesto': 1, 'puntos': puntos_por_posicion[1]}
        )
        TablaPosiciones.objects.update_or_create(
            deporte=deporte_clave, equipo=segundo_puesto,
            defaults={'puesto': 2, 'puntos': puntos_por_posicion[2]}
        )

        if tercer_puesto and cuarto_puesto:
            TablaPosiciones.objects.update_or_create(
                deporte=deporte_clave, equipo=tercer_puesto,
                defaults={'puesto': 3, 'puntos': puntos_por_posicion[3]}
            )
            TablaPosiciones.objects.update_or_create(
                deporte=deporte_clave, equipo=cuarto_puesto,
                defaults={'puesto': 4, 'puntos': puntos_por_posicion[4]}
            )

    # Obtener los datos de puntos y posiciones incluyendo la imagen
    equipos_con_datos = TablaPosiciones.objects.values(
        'equipo__nombre', 'equipo__imagen', 'deporte', 'puntos', 'puesto'
    ).distinct()

    equipos = {}

    for entry in equipos_con_datos:
        equipo_nombre = entry['equipo__nombre']
        equipo_imagen = entry['equipo__imagen']
        deporte_clave = entry['deporte']
        puntos = entry['puntos']
        puesto = entry['puesto']

        if equipo_nombre not in equipos:
            equipos[equipo_nombre] = {
                'posicion': puesto,
                'total': 0,
                'detalles': {},
                'imagen': equipo_imagen
            }

        # Aquí convertimos la clave del deporte al nombre legible
        deporte_nombre_legible = deportes_claves[deporte_clave]
        equipos[equipo_nombre]['detalles'][deporte_nombre_legible] = puntos
        equipos[equipo_nombre]['total'] += puntos

    equipos_ordenados = sorted(equipos.items(), key=lambda x: x[1]['total'], reverse=True)

    return render(request, 'tabla_posicionesfuo.html', {
        'equipos': equipos_ordenados,
        'deportes_nombres': [v for k, v in PartidoUnca.DEPORTE_CHOICES],  # Nombres legibles de deportes
    })















