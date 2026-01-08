from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    reorder_level = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"

class Project(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Completed', 'Completed'), ('On Hold', 'On Hold')]
    project_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class StockAllocation(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='allocations')
    quantity_allocated = models.IntegerField()
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity_allocated} {self.stock.item_name} -> {self.project.project_name}"