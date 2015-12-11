# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('problems', '0006_auto_20151211_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='dislike_vote_users',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='like_vote_users',
        ),
        migrations.AddField(
            model_name='solution',
            name='sol_dislike_vote_users',
            field=models.ManyToManyField(related_name='sol_dislike_vote_users', to='users.User'),
        ),
        migrations.AddField(
            model_name='solution',
            name='sol_like_vote_users',
            field=models.ManyToManyField(related_name='sol_like_vote_users', to='users.User'),
        ),
    ]
