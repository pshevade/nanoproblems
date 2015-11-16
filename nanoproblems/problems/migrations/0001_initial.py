# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('posted', models.DateField(auto_now_add=True)),
                ('category', models.CharField(default=b'CHALLENGE', max_length=15, choices=[(b'INTERVIEW', b'Interview Problem'), (b'CHALLENGE', b'Challenge Problem'), (b'QUESTION', b'The "I-have-a" Problem'), (b'CONTEST', b'Contest')])),
                ('difficulty', models.CharField(default=1, max_length=10, choices=[(b'EASY', b'Easy'), (b'MEDIUM', b'Medium'), (b'HARD', b'Hard')])),
                ('questions', models.ManyToManyField(to='comments.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=200)),
                ('description', models.TextField()),
                ('posted', models.DateField(auto_now_add=True)),
                ('comments', models.ManyToManyField(to='comments.Comment')),
                ('problem', models.ForeignKey(default=None, to='problems.Problem')),
                ('user', models.ForeignKey(default=None, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problems.Tag'),
        ),
        migrations.AddField(
            model_name='problem',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
        ),
    ]
