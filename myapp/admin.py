from django.contrib import admin
# Update these names to match your new models
from .models import Stock, Project, StockAllocation

admin.site.register(Stock)
admin.site.register(Project)
admin.site.register(StockAllocation)