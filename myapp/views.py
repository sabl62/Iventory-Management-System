from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Stock, Project, StockAllocation

@login_required
def dashboard(request):
    total_items = Stock.objects.count()
    low_stock = Stock.objects.filter(quantity__lt=F('reorder_level')).count()
    active_projects = Project.objects.filter(status='Active').count()
    
    context = {
        'total_items': total_items,
        'low_stock': low_stock,
        'active_projects': active_projects,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def main_stock(request):
    stocks = Stock.objects.all().order_by('item_name')
    return render(request, 'inventory/main_stock.html', {'stocks': stocks})

@login_required
def projects(request):
    # Moved this outside so it is a standalone function
    project_list = Project.objects.all()
    return render(request, 'inventory/projects.html', {'projects': project_list})

@login_required
def allocate_stock(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        project_id = request.POST.get('project_id')
        qty = int(request.POST.get('quantity'))

        stock_item = get_object_or_404(Stock, id=stock_id)
        project_item = get_object_or_404(Project, id=project_id)

        if stock_item.quantity >= qty:
            StockAllocation.objects.create(
                stock=stock_item,
                project=project_item,
                quantity_allocated=qty,
                allocated_by=request.user
            )
            stock_item.quantity -= qty
            stock_item.save()
            return redirect('dashboard')
            
    stocks = Stock.objects.all()
    # Note: Using a different variable name 'active_projects_list' to avoid
    # confusion with the 'projects' function name
    active_projects_list = Project.objects.filter(status='Active')
    return render(request, 'inventory/allocate.html', {
        'stocks': stocks, 
        'projects': active_projects_list
    })