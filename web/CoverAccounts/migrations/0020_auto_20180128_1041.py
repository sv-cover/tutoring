# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-28 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoverAccounts', '0019_auto_20180128_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covermember',
            name='telegram_chat_id',
            field=models.IntegerField(default=None),
        ),
    ]
