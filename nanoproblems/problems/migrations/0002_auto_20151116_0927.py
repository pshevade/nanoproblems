# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='questions',
        ),
        migrations.AddField(
            model_name='problem',
            name='comments',
            field=models.ManyToManyField(to='comments.Comment'),
        ),
    ]
