from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router dla API 
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'expenses', views.ExpenseViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_add, name='expense_add'),
    path('expenses/<int:id>/', views.expense_detail, name='expense_detail'),
    path('expenses/<int:id>/edit/', views.expense_edit, name='expense_edit'),
    path('expenses/<int:id>/delete/', views.expense_delete, name='expense_delete'),
    path('expenses/category/<str:category>/', views.expenses_by_category, name='expenses_by_category'),
    path('expenses/year/<int:year>/', views.expenses_by_year, name='expenses_by_year'),
    path('incomes/', views.income_list, name='income_list'),
    path('incomes/add/', views.income_add, name='income_add'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_add, name='budget_add'),
    path('incomes/<int:id>/edit/', views.income_edit, name='income_edit'),
    path('incomes/<int:id>/delete/', views.income_delete, name='income_delete'),
    path('budgets/<int:id>/edit/', views.budget_edit, name='budget_edit'),
    path('budgets/<int:id>/delete/', views.budget_delete, name='budget_delete'),

    # API endpoints
    path('api/', include(router.urls)),

    # JWT Token Authentication 
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]