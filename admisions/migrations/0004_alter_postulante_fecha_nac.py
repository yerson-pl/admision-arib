# Generated by Django 4.1.5 on 2023-03-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admisions', '0003_alter_postulante_fecha_nac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postulante',
            name='fecha_nac',
            field=models.DateField(blank=True, verbose_name='Fecha de Nacimiento (dd.MM.AAAA)'),
        ),
    ]
