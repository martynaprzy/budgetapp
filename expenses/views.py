# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets
from .models import Category, Expense, Income, Budget
from .serializers import CategorySerializer, ExpenseSerializer
from .forms import ExpenseForm, IncomeForm, BudgetForm
from django.utils import timezone

# API ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

# Home
def home(request):
    return render(request, 'expenses/index.html')

# CRUD
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

def expense_detail(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})

def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(initial={'date': timezone.now().date()})
    return render(request, 'expenses/expense_add.html', {'form': form})

def expense_edit(request, id):
    expense = get_object_or_404(Expense, id=id)
    form = ExpenseForm(request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/expense_edit.html', {'form': form})

def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

# Filtering views
def expenses_by_category(request, category):
    expenses = Expense.objects.filter(category__name=category).order_by('-date')
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'filter_title': f'Category: {category}'
    })

def expenses_by_year(request, year):
    expenses = Expense.objects.filter(date__year=year).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'filter_title': f'Expenses for {year}',
        'total_amount': total
    })

# Income views
def income_list(request):
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'expenses/income_list.html', {'incomes': incomes})

def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'expenses/income_add.html', {'form': form})

# Budget views
def budget_list(request):
    budgets = Budget.objects.all().order_by('-year', '-month')
    return render(request, 'expenses/budget_list.html', {'budgets': budgets})

def budget_add(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'expenses/budget_add.html', {'form': form})

# Income 
def income_edit(request, id):
    income = get_object_or_404(Income, id=id)
    form = IncomeForm(request.POST or None, instance=income)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('income_list')
    return render(request, 'expenses/income_edit.html', {'form': form})

def income_delete(request, id):
    income = get_object_or_404(Income, id=id)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'expenses/income_confirm_delete.html', {'income': income})

# Budget
def budget_edit(request, id):
    budget = get_object_or_404(Budget, id=id)
    form = BudgetForm(request.POST or None, instance=budget)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('budget_list')
    return render(request, 'expenses/budget_edit.html', {'form': form})

def budget_delete(request, id):
    budget = get_object_or_404(Budget, id=id)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'expenses/budget_confirm_delete.html', {'budget': budget})
