from django.db import models
# Create your models here.
class Adjustment(models.Model):
    AMOUNT_TYPE_CHOICES = [
        (1, 'adjustment'),
        (2, 'cash'),
    ]
    
    loan_id = models.IntegerField()
    from_book = models.IntegerField()
    to_book = models.IntegerField()
    loan_date = models.DateTimeField()
    loan_week = models.IntegerField()
    adjustment_week = models.IntegerField()
    adjustment_date = models.DateTimeField()
    amount = models.FloatField()
    amount_type = models.IntegerField(choices=AMOUNT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'adjustments'

    def __str__(self):
        return f'Adjustment {self.id} for Loan {self.loan_id}'