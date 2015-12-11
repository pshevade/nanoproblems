# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('problems', '0002_auto_20151123_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='vote_user',
            field=models.ManyToManyField(to='users.User'),
        ),
        migrations.AddField(
            model_name='solution',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='solution',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='solution',
            name='vote_users',
            field=models.ManyToManyField(to='users.User'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='user',
            field=models.ForeignKey(related_name='+', default=None, to='users.User'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(related_name='+', default=None, to='users.User'),
        ),
    ]
