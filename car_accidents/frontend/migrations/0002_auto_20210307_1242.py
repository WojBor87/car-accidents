# Generated by Django 3.1.7 on 2021-03-07 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accident',
            name='id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='lighting_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='place_of_the_event_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='road_geometry_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='road_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='type_of_accident_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='type_of_injury_id',
        ),
        migrations.RemoveField(
            model_name='accident',
            name='weather_conditions_id',
        ),
        migrations.AddField(
            model_name='accident',
            name='idksip',
            field=models.CharField(default='EWK-000000000', max_length=15, primary_key=True, serialize=False, verbose_name='Accident unique idksip key'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='lighting',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.lighting', verbose_name='Accident lighting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='place_of_the_event',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.placeoftheevent', verbose_name='Accident place_of_the_event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='road',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.road', verbose_name='Accident road'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='road_geometry',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.roadgeometry', verbose_name='Accident road_geometry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='type_of_accident',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.typeofaccident', verbose_name='Accident type_of_accident'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='type_of_injury',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.typeofinjury', verbose_name='Accident type_of_injury'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accident',
            name='weather_conditions',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.weatherconditions', verbose_name='Accident weather_conditions'),
            preserve_default=False,
        ),
    ]