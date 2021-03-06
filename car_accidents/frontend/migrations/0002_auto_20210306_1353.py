# Generated by Django 3.1.7 on 2021-03-06 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='is_built_up_area',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='accident',
            name='is_offender_intoxicated',
            field=models.BooleanField(),
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('is_city', models.BooleanField()),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.district')),
            ],
        ),
        migrations.AlterField(
            model_name='accident',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.town'),
        ),
    ]
