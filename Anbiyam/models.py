from django.db import models

# Create your models here.

class Anbiyam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    village = models.CharField(max_length=60)
    collection_agent = models.CharField(max_length=50)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'anbiyam'

    def __str__(self):
        return self.name