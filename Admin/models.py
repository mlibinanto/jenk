from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Admin(models.Model):
    ROLE_CHOICES = [
        (1, 'Admin'),
        (2, 'Cashier'),
        (3, 'Accountant'),
    ]
    
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    password = models.TextField()
    role = models.IntegerField(choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.TextField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admin'
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Hash and set password using Argon2"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verify password using Argon2"""
        return check_password(raw_password, self.password)