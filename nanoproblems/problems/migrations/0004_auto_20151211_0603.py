# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20151211_0545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='vote_user',
            new_name='vote_users',
        ),
    ]
