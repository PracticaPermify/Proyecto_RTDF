# Generated by Django 4.0.6 on 2023-09-27 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtdf', '0030_alter_pautaterapeutica_fk_informe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='fk_origen_audio',
            field=models.ForeignKey(db_column='fk_origen_audio', on_delete=django.db.models.deletion.PROTECT, to='rtdf.origenaudio'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='fk_pauta_terapeutica',
            field=models.ForeignKey(db_column='fk_pauta_terapeutica', on_delete=django.db.models.deletion.CASCADE, to='rtdf.pautaterapeutica'),
        ),
        migrations.AlterField(
            model_name='audioscoeficientes',
            name='fk_tipo_llenado',
            field=models.ForeignKey(db_column='fk_tipo_llenado', on_delete=django.db.models.deletion.PROTECT, to='rtdf.tpllenado'),
        ),
        migrations.AlterField(
            model_name='audioscoeficientes',
            name='id_audio',
            field=models.ForeignKey(db_column='id_audio', on_delete=django.db.models.deletion.CASCADE, to='rtdf.audio'),
        ),
        migrations.AlterField(
            model_name='comuna',
            name='id_provincia',
            field=models.ForeignKey(db_column='id_provincia', on_delete=django.db.models.deletion.CASCADE, to='rtdf.provincia'),
        ),
        migrations.AlterField(
            model_name='familiarpaciente',
            name='fk_tipo_familiar',
            field=models.ForeignKey(db_column='fk_tipo_familiar', default=1, on_delete=django.db.models.deletion.PROTECT, to='rtdf.tpfamiliar'),
        ),
        migrations.AlterField(
            model_name='familiarpaciente',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='institucion',
            name='id_comuna',
            field=models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.CASCADE, to='rtdf.comuna'),
        ),
        migrations.AlterField(
            model_name='intensidad',
            name='id_pauta_terapeutica',
            field=models.OneToOneField(db_column='id_pauta_terapeutica', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rtdf.pautaterapeutica'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fk_tipo_diabetes',
            field=models.ForeignKey(db_column='fk_tipo_diabetes', on_delete=django.db.models.deletion.PROTECT, to='rtdf.tipodiabetes'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fk_tipo_hipertension',
            field=models.ForeignKey(db_column='fk_tipo_hipertension', on_delete=django.db.models.deletion.PROTECT, to='rtdf.tipohipertension'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='preregistro',
            name='id_comuna',
            field=models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.PROTECT, to='rtdf.comuna'),
        ),
        migrations.AlterField(
            model_name='preregistro',
            name='id_institucion',
            field=models.ForeignKey(db_column='id_institucion', on_delete=django.db.models.deletion.PROTECT, to='rtdf.institucion'),
        ),
        migrations.AlterField(
            model_name='preregistro',
            name='id_tp_usuario',
            field=models.ForeignKey(db_column='id_tp_usuario', on_delete=django.db.models.deletion.PROTECT, to='rtdf.tpusuario'),
        ),
        migrations.AlterField(
            model_name='profesionalsalud',
            name='id_institucion',
            field=models.ForeignKey(db_column='id_institucion', on_delete=django.db.models.deletion.PROTECT, to='rtdf.institucion'),
        ),
        migrations.AlterField(
            model_name='profesionalsalud',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='provincia',
            name='id_region',
            field=models.ForeignKey(db_column='id_region', on_delete=django.db.models.deletion.CASCADE, to='rtdf.region'),
        ),
        migrations.AlterField(
            model_name='region',
            name='id_pais',
            field=models.ForeignKey(db_column='id_pais', on_delete=django.db.models.deletion.CASCADE, to='rtdf.pais'),
        ),
        migrations.AlterField(
            model_name='relacionfp',
            name='fk_familiar_paciente',
            field=models.ForeignKey(db_column='fk_familiar_paciente', on_delete=django.db.models.deletion.CASCADE, to='rtdf.familiarpaciente'),
        ),
        migrations.AlterField(
            model_name='relacionfp',
            name='id_paciente',
            field=models.ForeignKey(db_column='id_paciente', on_delete=django.db.models.deletion.CASCADE, to='rtdf.paciente'),
        ),
        migrations.AlterField(
            model_name='relacionpapro',
            name='fk_profesional_salud',
            field=models.ForeignKey(db_column='fk_profesional_salud', on_delete=django.db.models.deletion.CASCADE, to='rtdf.profesionalsalud'),
        ),
        migrations.AlterField(
            model_name='relacionpapro',
            name='id_paciente',
            field=models.ForeignKey(db_column='id_paciente', on_delete=django.db.models.deletion.CASCADE, to='rtdf.paciente'),
        ),
        migrations.AlterField(
            model_name='validacion',
            name='id_pre_registro',
            field=models.OneToOneField(db_column='id_pre_registro', on_delete=django.db.models.deletion.CASCADE, to='rtdf.preregistro'),
        ),
        migrations.AlterField(
            model_name='validacion',
            name='id_usuario',
            field=models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vocalizacion',
            name='id_pauta_terapeutica',
            field=models.OneToOneField(db_column='id_pauta_terapeutica', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rtdf.pautaterapeutica'),
        ),
    ]