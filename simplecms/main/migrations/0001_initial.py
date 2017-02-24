# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-createTime'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('pageType', models.CharField(max_length=10)),
                ('content', models.TextField(blank=True, null=True)),
                ('appPath', models.CharField(blank=True, max_length=255, null=True)),
                ('mainMenuOrder', models.IntegerField()),
                ('subMenuOrder', models.IntegerField(default=0)),
                ('thirdMenuOrder', models.IntegerField(default=0)),
                ('showTop', models.BooleanField(default=True)),
                ('showLeft', models.BooleanField(default=True)),
                ('showBottom', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['mainMenuOrder', 'subMenuOrder'],
            },
        ),
        migrations.AddField(
            model_name='listitem',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentPage', to='main.Page'),
        ),
    ]