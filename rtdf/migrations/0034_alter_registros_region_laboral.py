# Generated by Django 4.0.6 on 2023-10-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0033_vocalizacion_tempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registros',
            name='region_laboral',
            field=models.CharField(max_length=100),
        ),
    ]
