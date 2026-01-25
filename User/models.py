from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    book_no = models.IntegerField()
    name = models.TextField()
    anbiyam = models.IntegerField()
    village = models.TextField()
    guardian = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
    

class Weeks(models.Model):
    id = models.AutoField(primary_key=True)
    week = models.IntegerField()
    sunday_date = models.DateField()

    class Meta:
        db_table = 'weeks'

    def __str__(self):
        return f'Week {self.week} - {self.sunday_date}'