from django.db import models

# Create your models here.

class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    loan_no = models.IntegerField()
    user_id = models.IntegerField()
    book_no = models.IntegerField()
    anbiyam = models.IntegerField()
    week = models.IntegerField()
    status = models.IntegerField(choices=[(0, 'Awaiting Approval'), (1, 'Approved'), (2, 'Disbursed'), (3, 'Closed'), (4, 'Rejected')])
    is_eligible = models.IntegerField()
    approval_stats = models.TextField()
    amount = models.FloatField()
    balance_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    adjustment_status = models.IntegerField()

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return f'Loan {self.loan_no} for User {self.user_id}'