from django.urls import path
from .views import ExpenseListView, ExpenseDetailView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense_list'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('add/', ExpenseCreateView.as_view(), name='expense_create'),
    path('<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
