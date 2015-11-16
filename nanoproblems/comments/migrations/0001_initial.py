# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='comments.Comment')),
            ],
            bases=('comments.comment',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='comments.Comment')),
                ('resolved', models.BooleanField()),
            ],
            bases=('comments.comment',),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=None, to='comments.Question'),
        ),
    ]
