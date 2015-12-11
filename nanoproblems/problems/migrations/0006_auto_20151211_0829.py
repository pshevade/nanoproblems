# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20151211_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='dislike_vote_users',
            field=models.ManyToManyField(related_name='dislike_vote_users', to='users.User'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='like_vote_users',
            field=models.ManyToManyField(related_name='like_vote_users', to='users.User'),
        ),
    ]
