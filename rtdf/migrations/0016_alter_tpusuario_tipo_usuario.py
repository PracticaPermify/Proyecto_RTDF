# Generated by Django 4.0.6 on 2023-09-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0015_alter_tpusuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpusuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Paciente', 'Paciente'), ('Fonoaudiologo', 'Fonoaudiologo'), ('Familiar', 'Familiar'), ('Enfermera', 'Enfermera'), ('Neurologo', 'Neurologo')], max_length=30),
        ),
    ]