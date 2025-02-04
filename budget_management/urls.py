from django.contrib import admin
from django.urls import path, include
from expenses.views import expense_list, expense_add
from rest_framework import routers
from expenses.views import CategoryViewSet, ExpenseViewSet, ExpenseListView, ExpenseDetailView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView, monthly_summary
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

def home_view(request):
    return HttpResponse("<h1>Welcome to the Budget Management API</h1>")

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

