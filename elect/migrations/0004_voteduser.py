# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elect', '0003_remove_vote_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=128)),
            ],
        ),
    ]
