# Generated by Django 4.2.7 on 2023-12-02 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KPI1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_start_timestamp', models.BigIntegerField()),
                ('interval_end_timestamp', models.BigIntegerField()),
                ('service_id', models.IntegerField()),
                ('total_bytes', models.BigIntegerField()),
                ('interval', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='KPI2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_start_timestamp', models.BigIntegerField()),
                ('interval_end_timestamp', models.BigIntegerField()),
                ('cell_id', models.BigIntegerField()),
                ('number_of_unique_users', models.IntegerField()),
                ('interval', models.CharField(max_length=20)),
            ],
        ),
    ]
