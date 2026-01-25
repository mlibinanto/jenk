from django.db import models

# Create your models here.

class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    anbiyam = models.IntegerField()
    book_no = models.IntegerField()
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    week = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sunday_date = models.DateField()

    class Meta:
        db_table = 'collection'

    def __str__(self):
        return self.name