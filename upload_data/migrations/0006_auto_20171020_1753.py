# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_data', '0005_auto_20171013_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlmAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('fixed_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('available_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('consumption_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('mach_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('original_stock', models.IntegerField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('updat_time', models.DateTimeField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('frozen_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('next_consumption_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('next_sale_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('stock_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('rebate_integral', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('total_team_reward', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('total_sales_reward', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('qdl_team_bonus', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('qdl_sales_bonus', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('jxs_team_bonus', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('jxs_sales_bonus', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('qdl_total', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('qdl_get', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('jxs_total', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('jxs_get', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'flm_account',
            },
        ),
        migrations.CreateModel(
            name='UserLevelConfig',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=20)),
                ('level', models.IntegerField(unique=True)),
                ('max_price', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('next_level', models.IntegerField(unique=True)),
                ('opt_time', models.DateTimeField(auto_now_add=True)),
                ('provide_customer_service', models.SmallIntegerField()),
                ('provide_suggestion', models.SmallIntegerField()),
                ('status', models.SmallIntegerField()),
                ('tag_count', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'user_level_config',
            },
        ),
        migrations.CreateModel(
            name='Goods_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=50)),
                ('introduction', models.TextField()),
                ('upload_user_id', models.CharField(max_length=50)),
                ('upload_time', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('pic_file', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Superuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='bankbind',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='merchant_info',
            name='remark',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='withdraw_record',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='merchant_info',
            name='pic_file',
            field=models.TextField(),
        ),
    ]
