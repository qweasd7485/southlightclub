# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 03:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_page_thirdmenuoeder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['mainMenuOrder', 'subMenuOrder', 'thirdMenuOrder']},
        ),
        migrations.RenameField(
            model_name='page',
            old_name='thirdMenuOeder',
            new_name='thirdMenuOrder',
        ),
    ]