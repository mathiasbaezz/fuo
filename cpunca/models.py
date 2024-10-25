from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class EquipoUnca(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class PartidoUnca(models.Model):
    DEPORTE_CHOICES = (
        ('FUTBOL_FEMENINO', 'Fútbol de Campo Femenino'),
        ('FUTBOL_MASCULINO', 'Fútbol de Campo Masculino'),
        ('FUTSAL_FEMENINO', 'Fútsal FIFA Femenino'),
        ('FUTSAL_MASCULINO', 'Fútsal FIFA Masculino'),
        ('HANDBALL_FEMENINO', 'Handball Femenino'),
        ('HANDBALL_MASCULINO', 'Handball Masculino'),
        ('VOLLEY_FEMENINO', 'Volley Femenino'),
        ('VOLLEY_MASCULINO', 'Volley Masculino'),
        ('BASKET_FEMENINO', 'Basketball Femenino'),
        ('BASKET_MASCULINO', 'Basketball Masculino'),
        ('PADEL_FEMENINO', 'Padel Femenino'),
        ('PADEL_MASCULINO', 'Padel Masculino'),
        ('PIKI_FEMENINO', 'Piki Volley Femenino'),
        ('PIKI_MASCULINO', 'Piki Volley Masculino'),
        ('ATLETISMO', 'Atletismo'),
    )

    FASE_CHOICES = [
        ('Fase de Grupos', 'Fase de Grupos'),
        ('Octavos de Final', 'Octavos de Final'),
        ('Cuartos de Final', 'Cuartos de Final'),
        ('Semifinal', 'Semifinal'),
        ('Final', 'Final'),
    ]

    equipo_local = models.ForeignKey('EquipoUnca', on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey('EquipoUnca', on_delete=models.CASCADE, related_name='partidos_visitante')
    goles_local = models.PositiveIntegerField(blank=True, null=True)
    goles_visitante = models.PositiveIntegerField(blank=True, null=True)
    penales_local = models.PositiveIntegerField(blank=True, null=True)
    penales_visitante = models.PositiveIntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    partido_numero = models.CharField(max_length=99, blank=True, null=True)
    fase_partido = models.CharField(max_length=99, choices=FASE_CHOICES, blank=True, null=True)
    deporte = models.CharField(max_length=50, choices=DEPORTE_CHOICES, blank=True, null=True)
    informe_final = models.CharField(max_length=99, blank=True, null=True)

    def __str__(self):
        return f"PartidoUnca {self.id} {self.equipo_local} vs {self.equipo_visitante}"

    def get_absolute_url(self):
        return reverse('resumen_unca', kwargs={'pk': self.pk})




class EventoPartidoUnca(models.Model):
    PARTIDO_EVENT_CHOICES = (
        ('INICIO DEL PARTIDO', 'Inicio del partido'),
        ('PENDIENTE', 'Pendiente'),
        ('FINAL DEL PARTIDO', 'Fin del partido'),
    )

    partido = models.ForeignKey(PartidoUnca, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=PARTIDO_EVENT_CHOICES)
    minuto = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} en el minuto {self.minuto} del partido {self.partido}"


class EventosUnca(models.Model):
    PARTIDO_EVENT_CHOICES = (
        ('GOOOOL', 'Gol local'),
        ('GOOOL', 'Gol visitante'),
        ('PUNTO', 'Punto local'),
        ('PUNTO ', 'Punto visitante'),
        ('TARJETA ROJA', 'Tarjeta roja local'),
        ('TARJETA ROJA ', 'Tarjeta roja visitante'),
        ('TARJETA AMARILLA', 'Tarjeta amarilla local'),
        ('TARJETA AMARILLA ', 'Tarjeta amarilla visitante'),
    )

    partido = models.ForeignKey(PartidoUnca, on_delete=models.CASCADE)
    minuto = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100, choices=PARTIDO_EVENT_CHOICES)
    jugadores = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.tipo} en el minuto {self.minuto} del partido {self.partido}"


class TablaPosiciones(models.Model):
    deporte = models.CharField(max_length=50, choices=PartidoUnca.DEPORTE_CHOICES)
    equipo = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE)
    puesto = models.PositiveIntegerField()  # 1, 2, 3 o 4
    puntos = models.PositiveIntegerField()  # 20, 15, 10, 5 según puesto

    def __str__(self):
        return f"{self.equipo.nombre} - {self.deporte} - Puesto {self.puesto} con {self.puntos} puntos"

    class Meta:
        unique_together = ('deporte', 'equipo', 'puesto')



class TercerPuestoLogica:
    @staticmethod
    def determinar_tercer_puesto(semifinales):
        # semifinales: lista de partidos de la fase semifinal
        perdedores = []
        for partido in semifinales:
            if partido.goles_local < partido.goles_visitante:
                perdedores.append((partido.equipo_local, partido.goles_visitante - partido.goles_local))
            else:
                perdedores.append((partido.equipo_visitante, partido.goles_local - partido.goles_visitante))

        # Ordenamos los perdedores por la diferencia de goles (menor diferencia de goles es mejor)
        perdedores.sort(key=lambda x: x[1])

        # Si empatan en diferencia de goles, entonces revisamos fases anteriores
        if perdedores[0][1] == perdedores[1][1]:
            equipo1 = perdedores[0][0]
            equipo2 = perdedores[1][0]

            # Verificar resultados en fases previas
            equipo1_victorias, equipo1_dif_goles, equipo1_tarjetas = TercerPuestoLogica.obtener_estadisticas_previas(equipo1)
            equipo2_victorias, equipo2_dif_goles, equipo2_tarjetas = TercerPuestoLogica.obtener_estadisticas_previas(equipo2)

            # Comparar partidos ganados
            if equipo1_victorias > equipo2_victorias:
                tercer_puesto = equipo1
                cuarto_puesto = equipo2
            elif equipo2_victorias > equipo1_victorias:
                tercer_puesto = equipo2
                cuarto_puesto = equipo1
            else:
                # Si están empatados en victorias, comparamos diferencia de goles acumulada
                if equipo1_dif_goles > equipo2_dif_goles:
                    tercer_puesto = equipo1
                    cuarto_puesto = equipo2
                elif equipo2_dif_goles > equipo1_dif_goles:
                    tercer_puesto = equipo2
                    cuarto_puesto = equipo1
                else:
                    # Si siguen empatados, comparamos tarjetas
                    if equipo1_tarjetas < equipo2_tarjetas:
                        tercer_puesto = equipo1
                        cuarto_puesto = equipo2
                    else:
                        tercer_puesto = equipo2
                        cuarto_puesto = equipo1

        else:
            tercer_puesto = perdedores[0][0]
            cuarto_puesto = perdedores[1][0]

        return tercer_puesto, cuarto_puesto

    @staticmethod
    def obtener_estadisticas_previas(equipo):
        """
        Esta función obtiene estadísticas de las fases previas para el equipo dado.
        Devuelve:
        - Cantidad de victorias en fases previas.
        - Diferencia de goles acumulada en fases previas.
        - Cantidad de tarjetas amarillas y rojas (ponderadas).
        """
        partidos_previos = PartidoUnca.objects.filter(
            Q(equipo_local=equipo) | Q(equipo_visitante=equipo),
            fase_partido__in=['Fase de Grupos', 'Octavos de Final', 'Cuartos de Final']
        )

        victorias = 0
        dif_goles_acumulada = 0
        tarjetas = 0  # Tarjetas amarillas = 1 punto, tarjetas rojas = 3 puntos

        for partido in partidos_previos:
            if partido.equipo_local == equipo:
                if partido.goles_local > partido.goles_visitante:
                    victorias += 1
                dif_goles_acumulada += partido.goles_local - partido.goles_visitante
            else:
                if partido.goles_visitante > partido.goles_local:
                    victorias += 1
                dif_goles_acumulada += partido.goles_visitante - partido.goles_local

            # Sumar tarjetas (deberás tener en cuenta cómo están almacenadas las tarjetas en tu modelo de eventos)
            eventos = EventosUnca.objects.filter(partido=partido, jugadores__icontains=equipo.nombre)
            for evento in eventos:
                if 'TARJETA AMARILLA' in evento.tipo:
                    tarjetas += 1
                elif 'TARJETA ROJA' in evento.tipo:
                    tarjetas += 3

        return victorias, dif_goles_acumulada, tarjetas






class CampeonUnca(models.Model):
    equipo = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE)
    campeon_2016 = models.IntegerField(default=0,)
    campeon_2017 = models.IntegerField(default=0)
    campeon_2018 = models.IntegerField(default=0)
    campeon_2019 = models.IntegerField(default=0)
    campeon_2022 = models.IntegerField(default=0)
    campeon_2023 = models.IntegerField(default=0)
    total_campeonatos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.equipo}"

class TablaPosicionesUnca(models.Model):
    equipo = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)
    partidos_jugados = models.PositiveIntegerField(default=0)
    partidos_ganados = models.PositiveIntegerField(default=0)
    partidos_empatados = models.PositiveIntegerField(default=0)
    partidos_perdidos = models.PositiveIntegerField(default=0)
    goles_favor = models.PositiveIntegerField(default=0)
    goles_contra = models.PositiveIntegerField(default=0)
    diferencia_goles = models.IntegerField(default=0)
    @staticmethod
    def calcular_posiciones():
        equipos = EquipoUnca.objects.all()
        TablaPosicionesUnca.objects.all().delete()
        for equipo in equipos:
            partidos_local = PartidoUnca.objects.filter(equipo_local=equipo)
            partidos_visitante = PartidoUnca.objects.filter(equipo_visitante=equipo)
            partidos_jugados = partidos_local.count() + partidos_visitante.count()
            partidos_ganados = partidos_local.filter(goles_local__gt=models.F('goles_visitante')).count()
            partidos_ganados += partidos_visitante.filter(goles_visitante__gt=models.F('goles_local')).count()
            partidos_empatados = partidos_local.filter(goles_local=models.F('goles_visitante')).count()
            partidos_empatados += partidos_visitante.filter(goles_visitante=models.F('goles_local')).count()
            partidos_perdidos = partidos_jugados - partidos_ganados - partidos_empatados
            goles_favor = partidos_local.aggregate(total=models.Sum('goles_local'))['total'] or 0
            goles_favor += partidos_visitante.aggregate(total=models.Sum('goles_visitante'))['total'] or 0
            goles_contra = partidos_local.aggregate(total=models.Sum('goles_visitante'))['total'] or 0
            goles_contra += partidos_visitante.aggregate(total=models.Sum('goles_local'))['total'] or 0
            puntos = partidos_ganados * 3 + partidos_empatados
            diferencia_goles = goles_favor - goles_contra
            TablaPosicionesUnca.objects.create(
                equipo=equipo,
                puntos=puntos,
                partidos_jugados=partidos_jugados,
                partidos_ganados=partidos_ganados,
                partidos_empatados=partidos_empatados,
                partidos_perdidos=partidos_perdidos,
                goles_favor=goles_favor,
                goles_contra=goles_contra,
                diferencia_goles=diferencia_goles
            )
@receiver(post_save, sender=PartidoUnca)
def actualizar_tabla_posiciones(sender, instance, **kwargs):
    TablaPosicionesUnca.calcular_posiciones()


class DeporteUnca(models.Model):
    foto = models.ImageField(null=True, blank=True)
    nombre = models.CharField(max_length=300)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class ChampionUnca(models.Model):
    foto = models.ImageField(null=True, blank=True)
    nombre = models.CharField(max_length=300)
    link = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.nombre

class ChampiongralUnca(models.Model):
    foto = models.ImageField(null=True, blank=True)
    nombre = models.CharField(max_length=300)
    link = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.nombre


class Categoria1 (models.Model):
    nombre = models.CharField(null= False, blank= True, max_length=100)

    def __str__(self):
        return self.nombre


class Categoria2 (models.Model):
    nombre = models.CharField(null= False, blank= True, max_length=100)

    def __str__(self):
        return self.nombre

class Categoria3 (models.Model):
    nombre = models.CharField(null= False, blank= True, max_length=100)

    def __str__(self):
        return self.nombre


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    categoria1 = models.ForeignKey('Categoria1', on_delete=models.CASCADE,null=True)
    categoria2 = models.ForeignKey ('Categoria2', on_delete=models.CASCADE, null=True)
    categoria3 = models.ForeignKey('Categoria3', on_delete=models.CASCADE, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    slug= models.SlugField(null=False, default="#")

    def get_absolute_url(self):
        return reverse('single_blog', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class AtletismoFeso(models.Model):
    DEPORTE_ATLETISMO_CHOICES = (
        ('100M_FEMENINO', '100m Femenino'),
        ('100M_MASCULINO', '100m Masculino'),
        ('200M_FEMENINO', '200m Femenino'),
        ('200M_MASCULINO', '200m Masculino'),
        ('400M_FEMENINO', '400m Femenino'),
        ('400M_MASCULINO', '400m Masculino'),
        ('800M_FEMENINO', '800m Femenino'),
        ('1500M_MASCULINO', '1500m Masculino'),
        ('4X100M_FEMENINO', '4x100m Femenino'),
        ('4X100M_MASCULINO', '4x100m Masculino'),
        ('DISCO_FEMENINO', 'Disco Femenino'),
        ('DISCO_MASCULINO', 'Disco Masculino'),
        ('BALA_FEMENINO', 'Bala Femenino'),
        ('BALA_MASCULINO', 'Bala Masculino'),
        ('JABALINA_FEMENINO', 'Jabalina Femenino'),
        ('JABALINA_MASCULINO', 'Jabalina Masculino'),
        ('SALTO_ALTO_FEMENINO', 'Salto Alto Femenino'),
        ('SALTO_ALTO_MASCULINO', 'Salto Alto Masculino'),
        ('SALTO_LARGO_FEMENINO', 'Salto Largo Femenino'),
        ('SALTO_LARGO_MASCULINO', 'Salto Largo Masculino'),
        ('SALTO_TRIPLE_FEMENINO', 'Salto Triple Femenino'),
        ('SALTO_TRIPLE_MASCULINO', 'Salto Triple Masculino'),
        ('CICLISMO_FEMENINO', 'Ciclismo Femenino'),
        ('CICLISMO_MASCULINO', 'Ciclismo Masculino'),
        ('NATACION_CROL_FEMENINO', 'Natacion Crol Femenino'),
        ('NATACION_CROL_MASCULINO', 'Natacion Crol Masculino'),
        ('NATACION_ESPALDA_FEMENINO', 'Natacion Espalda Femenino'),
        ('NATACION_ESPALDA_MASCULINO', 'Natacion Espalda Masculino'),
    )


    primer_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='primer_puesto')
    primer_puesto_atleta= models.CharField( max_length=50,  blank=True, null=True)
    segundo_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='segundo_puesto')
    segundo_puesto_atleta = models.CharField(max_length=50, blank=True, null=True)
    tercer_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='tercer_puesto')
    tercer_puesto_atleta = models.CharField(max_length=50, blank=True, null=True)
    cuarto_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='cuarto_puesto')
    cuarto_puesto_atleta = models.CharField(max_length=50, blank=True, null=True)
    quinto_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='quinto_puesto')
    quinto_puesto_atleta = models.CharField(max_length=50, blank=True, null=True)
    sexto_puesto = models.ForeignKey(EquipoUnca, on_delete=models.CASCADE, related_name='sexto_puesto')
    sexto_puesto_atleta = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    deporte = models.CharField(max_length=50, choices=DEPORTE_ATLETISMO_CHOICES, blank=True, null=True)


    def __str__(self):
        return f"AtletismoFeso {self.id}"
