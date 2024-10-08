# Generated by Django 5.1.1 on 2024-09-09 01:41

import TP_DECOM_SD.EnvioDoc.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('autores', models.CharField(max_length=255)),
                ('resumo', models.TextField()),
                ('palavras_chave', models.CharField(max_length=255)),
                ('data_publicacao', models.PositiveIntegerField(validators=[TP_DECOM_SD.EnvioDoc.models.validar_ano])),
                ('revista', models.CharField(max_length=255)),
                ('arquivo', models.FileField(upload_to='documentos/')),
            ],
        ),
    ]
