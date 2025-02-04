import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')  # Data od
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')   # Data do

    class Meta:
        model = Expense
        fields = ['category', 'start_date', 'end_date']
