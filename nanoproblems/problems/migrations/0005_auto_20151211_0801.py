# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('problems', '0004_auto_20151211_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='vote_users',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='vote_users',
        ),
        migrations.AddField(
            model_name='problem',
            name='dislike_vote_users',
            field=models.ManyToManyField(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='problem',
            name='like_vote_users',
            field=models.ManyToManyField(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='solution',
            name='dislike_vote_users',
            field=models.ManyToManyField(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='solution',
            name='like_vote_users',
            field=models.ManyToManyField(related_name='+', to='users.User'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
        ),
    ]
