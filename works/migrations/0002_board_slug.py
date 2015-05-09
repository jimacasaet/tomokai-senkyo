# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='slug',
            field=models.SlugField(default='none', unique=True),
            preserve_default=False,
        ),
    ]
