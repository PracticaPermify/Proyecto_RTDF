# Generated by Django 4.0.6 on 2023-10-25 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0034_alter_registros_region_laboral'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscalaVocales',
            fields=[
                ('id_pauta_terapeutica', models.OneToOneField(db_column='id_pauta_terapeutica', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rtdf.pautaterapeutica')),
                ('palabras', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'escala vocales',
                'db_table': 'escala_vocales',
            },
        ),
        migrations.CreateModel(
            name='PalabrasPacientes',
            fields=[
                ('id_palabras_pacientes', models.AutoField(primary_key=True, serialize=False)),
                ('palabras_paciente', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'palabras pacientes',
                'db_table': 'palabras_pacientes',
            },
        ),
    ]
