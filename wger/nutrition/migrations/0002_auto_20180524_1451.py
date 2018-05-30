# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-05-24 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='status',
            field=models.CharField(choices=[('1', 'Pending'), ('2', 'Accepted'), ('3', 'Declined'), ('4', 'Submitted by administrator'), ('5', 'System ingredient')], default='1', editable=False, max_length=2),
        ),
        migrations.AlterField(
            model_name='meal',
            name='order',
            field=models.IntegerField(blank=True, editable=False, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='mealitem',
            name='order',
            field=models.IntegerField(blank=True, editable=False, verbose_name='Order'),
        ),
    ]
