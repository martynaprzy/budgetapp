from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.amount} PLN"
    
    def get_absolute_url(self):
        # Przekierowanie na stronę szczegółów obiektu
        return reverse('expense_detail', args=[str(self.id)])

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Budżet na {self.month}: {self.limit} PLN"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.source} - {self.amount} PLN"