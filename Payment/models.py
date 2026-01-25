from django.db import models

# Create your models here.

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    loan_id = models.IntegerField()
    book_no = models.IntegerField()
    week = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'Payment {self.id} for Loan {self.loan_id}'