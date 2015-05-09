# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0002_board_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='slug',
        ),
    ]
