# Generated by Django 4.2.7 on 2023-12-03 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commSquareApi', '0002_alter_kpi1_options_alter_kpi2_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='kpi1',
            table='KPI1',
        ),
        migrations.AlterModelTable(
            name='kpi2',
            table='KPI2',
        ),
    ]
