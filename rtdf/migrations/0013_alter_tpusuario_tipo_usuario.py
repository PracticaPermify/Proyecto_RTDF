# Generated by Django 4.0.6 on 2023-09-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0012_alter_usuario_id_tp_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpusuario',
            name='tipo_usuario',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'Paciente'), (3, 'Fonoaudiologo'), (4, 'Familiar'), (5, 'Enfermera'), (6, 'Neurologo')], max_length=30),
        ),
    ]