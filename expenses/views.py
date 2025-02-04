# Django
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
# Aplikacja lokalna
from .models import Category, Expense, Income
from .serializers import CategorySerializer, ExpenseSerializer
from .filters import ExpenseFilter
from .forms import ExpenseForm
from datetime import datetime


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]  # Uwierzytelnianie
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'date']  # Filtrowanie po polach
    ordering_fields = ['date', 'amount']  # Sortowanie
    ordering = ['date']  # Domyślne sortowanie
    filterset_class = ExpenseFilter  # Użycie niestandardowego filtra

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response({"error": "Month and year are required parameters"}, status=400)

        summary = (
            Expense.objects.filter(date__year=year, date__month=month)
            .values('category__name')
            .annotate(total_amount=Sum('amount'))
        )
        return Response(summary)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Lista obiektów
class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

class IncomeListView(ListView):
    model = Income
    template_name = 'expenses/income_list.html'
    context_object_name = 'incomes'


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'

# Tworzenie, edycja, usuwanie
class ExpenseCreateView(CreateView):
    model = Expense
    fields = ['category', 'name', 'amount', 'date']
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')  # Przekierowanie na listę wydatków


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['category', 'name', 'amount', 'date']
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')  # Przekierowanie na listę wydatków


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

@login_required
def expense_list(request):
    """Wyświetla listę wydatków."""
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

def expense_add(request):
    """Dodaje nowy wydatek."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Przypisz zalogowanego użytkownika
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_add.html', {'form': form})

def monthly_summary(request, year, month):
    expenses = Expense.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    ).values('category__name').annotate(total=Sum('amount'))
    return JsonResponse(list(expenses), safe=False)
