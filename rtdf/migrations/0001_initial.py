# Generated by Django 4.0.6 on 2023-08-31 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id_audio', models.AutoField(primary_key=True, serialize=False)),
                ('url_audio', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'audio',
            },
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id_comuna', models.AutoField(primary_key=True, serialize=False)),
                ('comuna', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'comuna',
            },
        ),
        migrations.CreateModel(
            name='FamiliarPaciente',
            fields=[
                ('id_familiar_paciente', models.AutoField(primary_key=True, serialize=False)),
                ('parentesco', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'familiar_paciente',
            },
        ),
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('id_informe', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField()),
                ('observacion', models.TextField()),
            ],
            options={
                'db_table': 'informe',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id_institucion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_institucion', models.CharField(max_length=20)),
                ('id_comuna', models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.comuna')),
            ],
            options={
                'db_table': 'institucion',
            },
        ),
        migrations.CreateModel(
            name='OrigenAudio',
            fields=[
                ('id_origen_audio', models.AutoField(primary_key=True, serialize=False)),
                ('origen_audio', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'origen_audio',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id_paciente', models.AutoField(primary_key=True, serialize=False)),
                ('telegram', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'paciente',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id_pais', models.AutoField(primary_key=True, serialize=False)),
                ('pais', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'pais',
            },
        ),
        migrations.CreateModel(
            name='PautaTerapeutica',
            fields=[
                ('id_pauta_terapeutica', models.AutoField(primary_key=True, serialize=False)),
                ('cant_veces_dia', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('url_video', models.CharField(blank=True, max_length=200, null=True)),
                ('comentario', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'pauta_terapeutica',
            },
        ),
        migrations.CreateModel(
            name='PreRegistro',
            fields=[
                ('id_pre_registro', models.AutoField(primary_key=True, serialize=False)),
                ('numero_identificacion', models.CharField(max_length=100, unique=True)),
                ('primer_nombre', models.CharField(max_length=30)),
                ('segundo_nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('ap_paterno', models.CharField(max_length=30)),
                ('ap_materno', models.CharField(max_length=30)),
                ('fecha_nacimiento', models.DateTimeField()),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('numero_telefonico', models.CharField(blank=True, max_length=20, null=True)),
                ('validado', models.CharField(max_length=1)),
                ('id_comuna', models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.comuna')),
                ('id_institucion', models.ForeignKey(db_column='id_institucion', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.institucion')),
            ],
            options={
                'db_table': 'pre_registro',
            },
        ),
        migrations.CreateModel(
            name='ProfesionalSalud',
            fields=[
                ('id_profesional_salud', models.AutoField(primary_key=True, serialize=False)),
                ('profesional_salud', models.CharField(blank=True, max_length=30, null=True)),
                ('id_institucion', models.ForeignKey(db_column='id_institucion', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.institucion')),
            ],
            options={
                'db_table': 'profesional_salud',
            },
        ),
        migrations.CreateModel(
            name='Registros',
            fields=[
                ('id_registros', models.AutoField(primary_key=True, serialize=False)),
                ('numero_identificacion', models.CharField(max_length=100)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('region_laboral', models.CharField(max_length=50)),
                ('titulo_profesional', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'registros',
            },
        ),
        migrations.CreateModel(
            name='TipoDiabetes',
            fields=[
                ('id_tipo_diabetes', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_diabetes', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'tipo_diabetes',
            },
        ),
        migrations.CreateModel(
            name='TipoHipertension',
            fields=[
                ('id_tipo_hipertension', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_hipertension', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'tipo_hipertension',
            },
        ),
        migrations.CreateModel(
            name='TpInforme',
            fields=[
                ('tp_informe_id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_informe', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tp_informe',
            },
        ),
        migrations.CreateModel(
            name='TpLlenado',
            fields=[
                ('id_tipo_llenado', models.AutoField(primary_key=True, serialize=False)),
                ('llenado', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tp_llenado',
            },
        ),
        migrations.CreateModel(
            name='TpTerapia',
            fields=[
                ('id_tp_terapia', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_terapia', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tp_terapia',
            },
        ),
        migrations.CreateModel(
            name='TpUsuario',
            fields=[
                ('id_tp_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_usuario', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tp_usuario',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('numero_identificacion', models.CharField(max_length=100, unique=True)),
                ('primer_nombre', models.CharField(max_length=30)),
                ('segundo_nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('ap_paterno', models.CharField(max_length=30)),
                ('ap_materno', models.CharField(max_length=30)),
                ('fecha_nacimiento', models.DateTimeField()),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('numero_telefonico', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='usuarios', to='auth.group', verbose_name='groups')),
                ('id_comuna', models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.comuna')),
                ('id_tp_usuario', models.ForeignKey(db_column='id_tp_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tpusuario')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuarios', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='Esv',
            fields=[
                ('id_informe', models.OneToOneField(db_column='id_informe', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='rtdf.informe')),
                ('total_esv', models.IntegerField()),
                ('limitacion', models.IntegerField()),
                ('emocional', models.IntegerField()),
                ('fisico', models.IntegerField()),
            ],
            options={
                'db_table': 'esv',
            },
        ),
        migrations.CreateModel(
            name='Grbas',
            fields=[
                ('id_informe', models.OneToOneField(db_column='id_informe', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='rtdf.informe')),
                ('grado_disfonia', models.CharField(max_length=30)),
                ('r_aspereza', models.CharField(max_length=30)),
                ('b_soplo', models.CharField(max_length=30)),
                ('a_debilidad', models.CharField(max_length=30)),
                ('s_tension', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'grbas',
            },
        ),
        migrations.CreateModel(
            name='Intensidad',
            fields=[
                ('id_pauta_terapeutica', models.OneToOneField(db_column='id_pauta_terapeutica', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='rtdf.pautaterapeutica')),
                ('intensidad', models.CharField(max_length=20)),
                ('min_db', models.IntegerField()),
                ('max_db', models.IntegerField()),
            ],
            options={
                'db_table': 'intensidad',
            },
        ),
        migrations.CreateModel(
            name='Rasati',
            fields=[
                ('id_informe', models.OneToOneField(db_column='id_informe', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='rtdf.informe')),
                ('ronquedad', models.CharField(max_length=10)),
                ('aspereza', models.CharField(max_length=10)),
                ('soplo', models.CharField(max_length=10)),
                ('astenia', models.CharField(max_length=10)),
                ('tension', models.CharField(max_length=10)),
                ('inestabilidad', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'rasati',
            },
        ),
        migrations.CreateModel(
            name='Vocalizacion',
            fields=[
                ('id_pauta_terapeutica', models.OneToOneField(db_column='id_pauta_terapeutica', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='rtdf.pautaterapeutica')),
                ('duracion_seg', models.IntegerField()),
                ('bpm', models.IntegerField()),
            ],
            options={
                'db_table': 'vocalizacion',
            },
        ),
        migrations.CreateModel(
            name='Validacion',
            fields=[
                ('id_validacion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_validacion', models.DateTimeField()),
                ('id_pre_registro', models.OneToOneField(db_column='id_pre_registro', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.preregistro')),
                ('id_usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.usuario')),
            ],
            options={
                'db_table': 'validacion',
            },
        ),
        migrations.CreateModel(
            name='RelacionPaPro',
            fields=[
                ('id_relacion_pa_pro', models.AutoField(primary_key=True, serialize=False)),
                ('fk_profesional_salud', models.ForeignKey(db_column='fk_profesional_salud', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.profesionalsalud')),
                ('id_paciente', models.ForeignKey(db_column='id_paciente', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.paciente')),
            ],
            options={
                'db_table': 'relacion_pa_pro',
            },
        ),
        migrations.CreateModel(
            name='RelacionFp',
            fields=[
                ('id_relacion_fp', models.AutoField(primary_key=True, serialize=False)),
                ('fk_familiar_paciente', models.ForeignKey(db_column='fk_familiar_paciente', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.familiarpaciente')),
                ('id_paciente', models.ForeignKey(db_column='id_paciente', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.paciente')),
            ],
            options={
                'db_table': 'relacion_fp',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id_region', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=50)),
                ('id_pais', models.ForeignKey(db_column='id_pais', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.pais')),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id_provincia', models.AutoField(primary_key=True, serialize=False)),
                ('provincia', models.CharField(max_length=50)),
                ('id_region', models.ForeignKey(db_column='id_region', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.region')),
            ],
            options={
                'db_table': 'provincia',
            },
        ),
        migrations.AddField(
            model_name='profesionalsalud',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.usuario'),
        ),
        migrations.AddField(
            model_name='preregistro',
            name='id_tp_usuario',
            field=models.ForeignKey(db_column='id_tp_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tpusuario'),
        ),
        migrations.AddField(
            model_name='pautaterapeutica',
            name='fk_relacion_pa_pro',
            field=models.ForeignKey(db_column='fk_relacion_pa_pro', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.relacionpapro'),
        ),
        migrations.AddField(
            model_name='pautaterapeutica',
            name='fk_tp_terapia',
            field=models.ForeignKey(db_column='fk_tp_terapia', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tpterapia'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='fk_tipo_diabetes',
            field=models.ForeignKey(db_column='fk_tipo_diabetes', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tipodiabetes'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='fk_tipo_hipertension',
            field=models.ForeignKey(db_column='fk_tipo_hipertension', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tipohipertension'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.usuario'),
        ),
        migrations.AddField(
            model_name='informe',
            name='fk_relacion_pa_pro',
            field=models.ForeignKey(db_column='fk_relacion_pa_pro', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.relacionpapro'),
        ),
        migrations.AddField(
            model_name='informe',
            name='id_audio',
            field=models.ForeignKey(blank=True, db_column='id_audio', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.audio'),
        ),
        migrations.AddField(
            model_name='informe',
            name='tp_informe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tpinforme'),
        ),
        migrations.AddField(
            model_name='familiarpaciente',
            name='id_usuario',
            field=models.OneToOneField(db_column='id_usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.usuario'),
        ),
        migrations.AddField(
            model_name='comuna',
            name='id_provincia',
            field=models.ForeignKey(db_column='id_provincia', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.provincia'),
        ),
        migrations.CreateModel(
            name='Audioscoeficientes',
            fields=[
                ('id_audiocoeficientes', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_archivo', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('f0', models.CharField(max_length=100)),
                ('f1', models.CharField(max_length=100)),
                ('f2', models.CharField(max_length=100)),
                ('f3', models.CharField(max_length=100)),
                ('f4', models.CharField(max_length=100)),
                ('intensidad', models.CharField(max_length=100)),
                ('hnr', models.CharField(max_length=100)),
                ('local_jitter', models.CharField(max_length=100)),
                ('local_absolute_jitter', models.CharField(max_length=100)),
                ('rap_jitter', models.CharField(max_length=100)),
                ('ppq5_jitter', models.CharField(max_length=100)),
                ('ddp_jitter', models.CharField(max_length=100)),
                ('local_shimmer', models.CharField(max_length=100)),
                ('local_db_shimmer', models.CharField(max_length=100)),
                ('apq3_shimmer', models.CharField(max_length=100)),
                ('aqpq5_shimmer', models.CharField(max_length=100)),
                ('apq11_shimmer', models.CharField(max_length=100)),
                ('fk_tipo_llenado', models.ForeignKey(db_column='fk_tipo_llenado', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.tpllenado')),
                ('id_audio', models.ForeignKey(db_column='id_audio', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.audio')),
            ],
            options={
                'db_table': 'audioscoeficientes',
            },
        ),
        migrations.AddField(
            model_name='audio',
            name='fk_origen_audio',
            field=models.ForeignKey(db_column='fk_origen_audio', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.origenaudio'),
        ),
        migrations.AddField(
            model_name='audio',
            name='fk_pauta_terapeutica',
            field=models.ForeignKey(db_column='fk_pauta_terapeutica', on_delete=django.db.models.deletion.DO_NOTHING, to='rtdf.pautaterapeutica'),
        ),
    ]
