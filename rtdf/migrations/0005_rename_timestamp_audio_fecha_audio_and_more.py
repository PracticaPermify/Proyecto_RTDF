# Generated by Django 4.0.6 on 2023-09-04 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0004_rename_grado_disfonia_grbas_g_grado_disfonia_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audio',
            old_name='timestamp',
            new_name='fecha_audio',
        ),
        migrations.RenameField(
            model_name='audioscoeficientes',
            old_name='timestamp',
            new_name='fecha_coeficiente',
        ),
        migrations.RenameField(
            model_name='profesionalsalud',
            old_name='profesional_salud',
            new_name='titulo_profesional',
        ),
    ]
