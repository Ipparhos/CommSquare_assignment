
from django.db import models

class KPI1(models.Model):
    interval_start_timestamp = models.BigIntegerField()
    interval_end_timestamp = models.BigIntegerField()
    service_id = models.IntegerField()
    total_bytes = models.BigIntegerField()
    interval = models.CharField(max_length=20)

class KPI2(models.Model):
    interval_start_timestamp = models.BigIntegerField()
    interval_end_timestamp = models.BigIntegerField()
    cell_id = models.BigIntegerField()
    number_of_unique_users = models.IntegerField()
    interval = models.CharField(max_length=20)