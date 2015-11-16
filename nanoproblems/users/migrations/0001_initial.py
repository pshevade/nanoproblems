# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(default=b'', max_length=100)),
                ('nickname', models.CharField(default=b'', max_length=50)),
                ('user_key', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('nanodegree', models.CharField(default=b'Developer', max_length=15, choices=[(b'FULLSTACK', b'FullStack Developer'), (b'FRONTEND', b'Frontend Developer'), (b'ANDROID', b'Android Developer'), (b'DATA ANALYST', b'Data Analyst'), (b'IOS DEVELOPER', b'IOS Developer')])),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('email', 'nickname')]),
        ),
    ]
