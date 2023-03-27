from django.db import models

# Create your models here.
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
# Define Google Drive Storage
#permission =  GoogleDriveFilePermission(
#   GoogleDrivePermissionRole.WRITER,
#   GoogleDrivePermissionType.USER,
#   "admision@iestparib.edu.pe"
#)

gd_storage = GoogleDriveStorage()


def upload_location(instance, filename):
    return "postulantes/%s/%s" % (instance.dni_num, filename)

class Postulante(models.Model):
    """Model definition for Postulante."""
    
    CARRERA_CHOICES=[ 
        ('CC', 'Contrucción Civil'),
        ('C' , 'Contabilidad'),
        ('EM', 'Explotación Minera'),
    ]
    
  
    
    GENERO_CHOICES=[
        ('M', 'M'),
        ('F', 'F'),
        
    ]

    # TODO: Define fields here
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    dni_num = models.IntegerField('N° DNI', unique=True, blank=False, null=False)
    ap_paterno = models.CharField('Apellido Paterno',max_length=100, blank=False, null=False)
    ap_materno = models.CharField('Apellido Materno',max_length=100, blank=False, null=False)
    nombre = models.CharField('Nombres', max_length=150, blank=False, null=False)
    sexo = models.CharField('Sexo', max_length=2,choices=GENERO_CHOICES)
    fecha_nac = models.DateField('Fecha de Nacimiento (dd/MM/AAAA)', auto_now=False, auto_now_add=False, blank=True)
    departamento = models.CharField('Departamento',max_length=80)
    provincia = models.CharField('Provincia',max_length=100)
    distrito = models.CharField('Distrito',max_length=150)
    direccion = models.CharField('Dirección',max_length=200)
    correo = models.EmailField('Correo', max_length=254, unique=True)
    inst_procedencia = models.CharField('Colegio de Procedencia',max_length=150)
    egreso = models.IntegerField('Año de egreso')
    celular = models.IntegerField('N° Celular')
    carrera = models.CharField('Primera opcion Programa de Estudios al que postula',max_length=2,choices=CARRERA_CHOICES)
    seg_carrera = models.CharField('Segunda Opcion Programa de Estudios al que postula',max_length=2,choices=CARRERA_CHOICES)
    foto = models.FileField('Foto',upload_to='maps/',storage=gd_storage)
    dni = models.FileField('Foto DNI', upload_to='maps/', blank=False, null=False, storage=gd_storage)
    certificado = models.FileField('FotoCertificado de Estudios', upload_to='maps', blank=False, null=False, storage=gd_storage)
    num_operacion = models.CharField('Cod. Voucher', max_length=20, unique=True)
    voucher = models.FileField('Foto Voucher', upload_to='maps/', blank=False, null=False, storage=gd_storage)
    dec_juarada = models.BooleanField(default=False, verbose_name='Declaro bajo juramento que los datos que consigno en la presente FICHA DE INSCRIPCIÓN, son verídicos y me remito para la confrontación con los documentos originales. De no ser correctos pierdo la vacante de admisión y renuncio a todo derecho que pueda obtener.')

    class Meta:
        """Meta definition for Postulante."""

        verbose_name = 'Postulante'
        verbose_name_plural = 'Postulantes'

    def __str__(self):
        """Unicode representation of Postulante."""
        return self.nombre