# Generated by Django 3.2 on 2023-01-05 02:22

import core.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='image',
            field=stdimage.models.StdImageField(force_min_size=False, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 127, 'width': 270}}, verbose_name='Imagem'),
        ),
    ]
