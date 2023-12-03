
from django.db import models

class KPI1(models.Model):
    id = models.IntegerField(primary_key=True)
    interval_start_timestamp = models.BigIntegerField()
    interval_end_timestamp = models.BigIntegerField()
    service_id = models.IntegerField()
    total_bytes = models.BigIntegerField()
    interval_period = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = "KPI1"

class KPI2(models.Model):
    id = models.IntegerField(primary_key=True)
    interval_start_timestamp = models.BigIntegerField()
    interval_end_timestamp = models.BigIntegerField()
    cell_id = models.BigIntegerField()
    number_of_unique_users = models.IntegerField()
    interval_period = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = "KPI2"