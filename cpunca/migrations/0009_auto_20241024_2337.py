# Generated by Django 3.2 on 2024-10-25 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpunca', '0008_auto_20240828_0202'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtletismoFeso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primer_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('segundo_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('tercer_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('cuarto_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('quinto_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('sexto_puesto_atleta', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('deporte', models.CharField(blank=True, choices=[('100M_FEMENINO', '100m Femenino'), ('100M_MASCULINO', '100m Masculino'), ('200M_FEMENINO', '200m Femenino'), ('200M_MASCULINO', '200m Masculino'), ('400M_FEMENINO', '400m Femenino'), ('400M_MASCULINO', '400m Masculino'), ('800M_FEMENINO', '800m Femenino'), ('1500M_MASCULINO', '1500m Masculino'), ('4X100M_FEMENINO', '4x100m Femenino'), ('4X100M_MASCULINO', '4x100m Masculino'), ('DISCO_FEMENINO', 'Disco Femenino'), ('DISCO_MASCULINO', 'Disco Masculino'), ('BALA_FEMENINO', 'Bala Femenino'), ('BALA_MASCULINO', 'Bala Masculino'), ('JABALINA_FEMENINO', 'Jabalina Femenino'), ('JABALINA_MASCULINO', 'Jabalina Masculino'), ('SALTO_ALTO_FEMENINO', 'Salto Alto Femenino'), ('SALTO_ALTO_MASCULINO', 'Salto Alto Masculino'), ('SALTO_LARGO_FEMENINO', 'Salto Largo Femenino'), ('SALTO_LARGO_MASCULINO', 'Salto Largo Masculino'), ('SALTO_TRIPLE_FEMENINO', 'Salto Triple Femenino'), ('SALTO_TRIPLE_MASCULINO', 'Salto Triple Masculino'), ('CICLISMO_FEMENINO', 'Ciclismo Femenino'), ('CICLISMO_MASCULINO', 'Ciclismo Masculino'), ('NATACION_CROL_FEMENINO', 'Natacion Crol Femenino'), ('NATACION_CROL_MASCULINO', 'Natacion Crol Masculino'), ('NATACION_ESPALDA_FEMENINO', 'Natacion Espalda Femenino'), ('NATACION_ESPALDA_MASCULINO', 'Natacion Espalda Masculino')], max_length=50, null=True)),
                ('cuarto_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuarto_puesto', to='cpunca.equipounca')),
                ('primer_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primer_puesto', to='cpunca.equipounca')),
                ('quinto_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quinto_puesto', to='cpunca.equipounca')),
                ('segundo_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segundo_puesto', to='cpunca.equipounca')),
                ('sexto_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sexto_puesto', to='cpunca.equipounca')),
                ('tercer_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tercer_puesto', to='cpunca.equipounca')),
            ],
        ),
        migrations.CreateModel(
            name='TablaPosiciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deporte', models.CharField(choices=[('FUTBOL_FEMENINO', 'Fútbol de Campo Femenino'), ('FUTBOL_MASCULINO', 'Fútbol de Campo Masculino'), ('FUTSAL_FEMENINO', 'Fútsal FIFA Femenino'), ('FUTSAL_MASCULINO', 'Fútsal FIFA Masculino'), ('HANDBALL_FEMENINO', 'Handball Femenino'), ('HANDBALL_MASCULINO', 'Handball Masculino'), ('VOLLEY_FEMENINO', 'Volley Femenino'), ('VOLLEY_MASCULINO', 'Volley Masculino'), ('BASKET_FEMENINO', 'Basketball Femenino'), ('BASKET_MASCULINO', 'Basketball Masculino'), ('PADEL_FEMENINO', 'Padel Femenino'), ('PADEL_MASCULINO', 'Padel Masculino'), ('PIKI_FEMENINO', 'Piki Volley Femenino'), ('PIKI_MASCULINO', 'Piki Volley Masculino'), ('ATLETISMO', 'Atletismo')], max_length=50)),
                ('puesto', models.PositiveIntegerField()),
                ('puntos', models.PositiveIntegerField()),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpunca.equipounca')),
            ],
            options={
                'unique_together': {('deporte', 'equipo', 'puesto')},
            },
        ),
        migrations.AddField(
            model_name='partidounca',
            name='informe_final',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='partidounca',
            name='penales_local',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partidounca',
            name='penales_visitante',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partidounca',
            name='deporte',
            field=models.CharField(blank=True, choices=[('FUTBOL_FEMENINO', 'Fútbol de Campo Femenino'), ('FUTBOL_MASCULINO', 'Fútbol de Campo Masculino'), ('FUTSAL_FEMENINO', 'Fútsal FIFA Femenino'), ('FUTSAL_MASCULINO', 'Fútsal FIFA Masculino'), ('HANDBALL_FEMENINO', 'Handball Femenino'), ('HANDBALL_MASCULINO', 'Handball Masculino'), ('VOLLEY_FEMENINO', 'Volley Femenino'), ('VOLLEY_MASCULINO', 'Volley Masculino'), ('BASKET_FEMENINO', 'Basketball Femenino'), ('BASKET_MASCULINO', 'Basketball Masculino'), ('PADEL_FEMENINO', 'Padel Femenino'), ('PADEL_MASCULINO', 'Padel Masculino'), ('PIKI_FEMENINO', 'Piki Volley Femenino'), ('PIKI_MASCULINO', 'Piki Volley Masculino'), ('ATLETISMO', 'Atletismo')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='partidounca',
            name='fase_partido',
            field=models.CharField(blank=True, choices=[('Fase de Grupos', 'Fase de Grupos'), ('Octavos de Final', 'Octavos de Final'), ('Cuartos de Final', 'Cuartos de Final'), ('Semifinal', 'Semifinal'), ('Final', 'Final')], max_length=99, null=True),
        ),
        migrations.AlterField(
            model_name='partidounca',
            name='partido_numero',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.DeleteModel(
            name='PosicionUnca',
        ),
    ]