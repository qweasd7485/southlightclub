# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_page_thirdmenuoeder'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='thirdMenuOeder',
            field=models.IntegerField(default=0),
        ),
    ]
