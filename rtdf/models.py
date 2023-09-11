from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

####Funcionalidades####

TIPO_USUARIO = [
        ('Admin', 'Admin'),
        ('Paciente', 'Paciente'),
        ('Fonoaudiologo', 'Fonoaudiologo'),
        ('Familiar', 'Familiar'),
        ('Enfermera', 'Enfermera'),
        ('Neurologo', 'Neurologo'),
    ]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
###Tablas del modelamiento creado

class Audio(models.Model):
    id_audio = models.AutoField(primary_key=True)
    url_audio = models.CharField(max_length=200)
    fecha_audio = models.DateTimeField()
    fk_origen_audio = models.ForeignKey('OrigenAudio', models.DO_NOTHING, db_column='fk_origen_audio')
    fk_pauta_terapeutica = models.ForeignKey('PautaTerapeutica', models.DO_NOTHING, db_column='fk_pauta_terapeutica')

    class Meta:
        db_table = 'audio'


class Audioscoeficientes(models.Model):
    id_audiocoeficientes = models.AutoField(primary_key=True)
    nombre_archivo = models.CharField(max_length=100)
    fecha_coeficiente = models.DateTimeField()
    f0 = models.CharField(max_length=100)
    f1 = models.CharField(max_length=100)
    f2 = models.CharField(max_length=100)
    f3 = models.CharField(max_length=100)
    f4 = models.CharField(max_length=100)
    intensidad = models.CharField(max_length=100)
    hnr = models.CharField(max_length=100)
    local_jitter = models.CharField(max_length=100)
    local_absolute_jitter = models.CharField(max_length=100)
    rap_jitter = models.CharField(max_length=100)
    ppq5_jitter = models.CharField(max_length=100)
    ddp_jitter = models.CharField(max_length=100)
    local_shimmer = models.CharField(max_length=100)
    local_db_shimmer = models.CharField(max_length=100)
    apq3_shimmer = models.CharField(max_length=100)
    aqpq5_shimmer = models.CharField(max_length=100)
    apq11_shimmer = models.CharField(max_length=100)
    fk_tipo_llenado = models.ForeignKey('TpLlenado', models.DO_NOTHING, db_column='fk_tipo_llenado')
    id_audio = models.ForeignKey(Audio, models.DO_NOTHING, db_column='id_audio')

    class Meta:
        db_table = 'audioscoeficientes'


class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    comuna = models.CharField(max_length=50)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia')

    class Meta:
        db_table = 'comuna'


class Esv(models.Model):
    id_informe = models.OneToOneField('Informe', models.DO_NOTHING, db_column='id_informe', primary_key=True)
    total_esv = models.IntegerField()
    limitacion = models.IntegerField()
    emocional = models.IntegerField()
    fisico = models.IntegerField()

    class Meta:
        db_table = 'esv'


class FamiliarPaciente(models.Model):
    id_familiar_paciente = models.AutoField(primary_key=True)
    parentesco = models.CharField(max_length=20)
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        db_table = 'familiar_paciente'


class Grbas(models.Model):
    id_informe = models.OneToOneField('Informe', models.DO_NOTHING, db_column='id_informe', primary_key=True)
    g_grado_disfonia = models.CharField(max_length=30)
    r_aspereza = models.CharField(max_length=30)
    b_soplo = models.CharField(max_length=30)
    a_debilidad = models.CharField(max_length=30)
    s_tension = models.CharField(max_length=30)

    class Meta:
        db_table = 'grbas'


class Informe(models.Model):
    id_informe = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    observacion = models.TextField()
    fk_relacion_pa_pro = models.ForeignKey('RelacionPaPro', models.DO_NOTHING, db_column='fk_relacion_pa_pro')
    id_audio = models.ForeignKey(Audio, models.DO_NOTHING, db_column='id_audio', blank=True, null=True)
    tp_informe = models.ForeignKey('TpInforme', models.DO_NOTHING)

    class Meta:
        db_table = 'informe'


class Institucion(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    nombre_institucion = models.CharField(max_length=50)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        db_table = 'institucion'


class Intensidad(models.Model):
    id_pauta_terapeutica = models.OneToOneField('PautaTerapeutica', models.DO_NOTHING, db_column='id_pauta_terapeutica', primary_key=True)
    intensidad = models.CharField(max_length=20)
    min_db = models.IntegerField()
    max_db = models.IntegerField()

    class Meta:
        db_table = 'intensidad'


class OrigenAudio(models.Model):
    id_origen_audio = models.AutoField(primary_key=True)
    origen_audio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    class Meta:
        db_table = 'origen_audio'


class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    telegram = models.CharField(max_length=30, blank=True, null=True)
    fk_tipo_hipertension = models.ForeignKey('TipoHipertension', models.DO_NOTHING, db_column='fk_tipo_hipertension')
    fk_tipo_diabetes = models.ForeignKey('TipoDiabetes', models.DO_NOTHING, db_column='fk_tipo_diabetes')
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        db_table = 'paciente'


class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=60)

    class Meta:
        db_table = 'pais'


class PautaTerapeutica(models.Model):
    id_pauta_terapeutica = models.AutoField(primary_key=True)
    cant_veces_dia = models.IntegerField()
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    url_video = models.CharField(max_length=200, blank=True, null=True)
    comentario = models.CharField(max_length=200)
    fk_tp_terapia = models.ForeignKey('TpTerapia', models.DO_NOTHING, db_column='fk_tp_terapia')
    fk_relacion_pa_pro = models.ForeignKey('RelacionPaPro', models.DO_NOTHING, db_column='fk_relacion_pa_pro')

    class Meta:
        db_table = 'pauta_terapeutica'


class PreRegistro(models.Model):
    id_pre_registro = models.AutoField(primary_key=True)
    numero_identificacion = models.CharField(unique=True, max_length=100)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    ap_paterno = models.CharField(max_length=30)
    ap_materno = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=120)
    numero_telefonico = models.CharField(max_length=20, blank=True, null=True)
    validado = models.CharField(max_length=1, default=0)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    id_tp_usuario = models.ForeignKey('TpUsuario', models.DO_NOTHING, db_column='id_tp_usuario')
    id_institucion = models.ForeignKey(Institucion, models.DO_NOTHING, db_column='id_institucion')

    class Meta:
        db_table = 'pre_registro'


class ProfesionalSalud(models.Model):
    id_profesional_salud = models.AutoField(primary_key=True)
    titulo_profesional = models.CharField(max_length=30, blank=True, null=True)
    id_institucion = models.ForeignKey(Institucion, models.DO_NOTHING, db_column='id_institucion')
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        db_table = 'profesional_salud'


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=50)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region')

    class Meta:
        db_table = 'provincia'


class Rasati(models.Model): 
    id_informe = models.OneToOneField(Informe, models.DO_NOTHING, db_column='id_informe', primary_key=True)
    r_ronquedad = models.CharField(max_length=10)
    a_aspereza = models.CharField(max_length=10)
    s_soplo = models.CharField(max_length=10)
    a_astenia = models.CharField(max_length=10)
    t_tension = models.CharField(max_length=10)
    i_inestabilidad = models.CharField(max_length=10)

    class Meta:
        db_table = 'rasati'


class Region(models.Model): 
    id_region = models.AutoField(primary_key=True)
    region = models.CharField(max_length=50)
    id_pais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='id_pais')

    class Meta:
        db_table = 'region'


class Registros(models.Model):
    id_registros = models.AutoField(primary_key=True)
    numero_identificacion = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=100)
    region_laboral = models.CharField(max_length=50)
    titulo_profesional = models.CharField(max_length=100)

    class Meta:
        db_table = 'registros'


class RelacionFp(models.Model):
    id_relacion_fp = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='id_paciente')
    fk_familiar_paciente = models.ForeignKey(FamiliarPaciente, models.DO_NOTHING, db_column='fk_familiar_paciente')

    class Meta:
        db_table = 'relacion_fp'


class RelacionPaPro(models.Model):
    id_relacion_pa_pro = models.AutoField(primary_key=True)
    fk_profesional_salud = models.ForeignKey(ProfesionalSalud, models.DO_NOTHING, db_column='fk_profesional_salud')
    id_paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='id_paciente')

    class Meta:
        db_table = 'relacion_pa_pro'


class TipoDiabetes(models.Model):
    id_tipo_diabetes = models.AutoField(primary_key=True)
    tipo_diabetes = models.CharField(max_length=10)

    class Meta:
        db_table = 'tipo_diabetes'

    def __str__(self):
        return self.tipo_diabetes


class TipoHipertension(models.Model):
    id_tipo_hipertension = models.AutoField(primary_key=True)
    tipo_hipertension = models.CharField(max_length=10)

    class Meta:
        db_table = 'tipo_hipertension'

    def __str__(self):
        return self.tipo_hipertension


class TpInforme(models.Model):
    tp_informe_id = models.AutoField(primary_key=True)
    tipo_informe = models.CharField(max_length=30)

    class Meta:
        db_table = 'tp_informe'


class TpLlenado(models.Model):
    id_tipo_llenado = models.AutoField(primary_key=True)
    llenado = models.CharField(max_length=20)

    class Meta:
        db_table = 'tp_llenado'


class TpTerapia(models.Model):
    id_tp_terapia = models.AutoField(primary_key=True)
    tipo_terapia = models.CharField(max_length=100)

    class Meta:
        db_table = 'tp_terapia'


class TpUsuario(models.Model):
    id_tp_usuario = models.AutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=30,choices=TIPO_USUARIO)
    
    class Meta:
        db_table = 'tp_usuario'

    def __str__(self):
        return self.tipo_usuario

class UsuarioManager(BaseUserManager):
    def create_user(self, numero_identificacion, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo "email" debe estar configurado')

        email = self.normalize_email(email)
        user = self.model(
            numero_identificacion=numero_identificacion,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_identificacion, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(numero_identificacion, email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    numero_identificacion = models.CharField(unique=True, max_length=100)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    ap_paterno = models.CharField(max_length=30)
    ap_materno = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    email = models.CharField(unique=True, max_length=100)
    #password = models.CharField(max_length=20) #Generado Automaticamente por Django
    numero_telefonico = models.CharField(max_length=20, blank=True, null=True)
    id_tp_usuario = models.ForeignKey(TpUsuario, on_delete=models.CASCADE, db_column='id_tp_usuario',default=1)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna',default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # related_name único para grupos y permisos. Problema con nombres de la clases internas de Django
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='usuarios'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='usuarios'
    )

    objects = UsuarioManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['numero_identificacion', 'primer_nombre', 'ap_paterno', 'ap_materno', 'fecha_nacimiento']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuario'


class Validacion(models.Model):
    id_validacion = models.AutoField(primary_key=True)
    fecha_validacion = models.DateTimeField()
    id_pre_registro = models.OneToOneField(PreRegistro, models.DO_NOTHING, db_column='id_pre_registro')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        db_table = 'validacion'


class Vocalizacion(models.Model):
    id_pauta_terapeutica = models.OneToOneField(PautaTerapeutica, models.DO_NOTHING, db_column='id_pauta_terapeutica', primary_key=True)
    duracion_seg = models.IntegerField()
    bpm = models.IntegerField()

    class Meta:
        db_table = 'vocalizacion'
