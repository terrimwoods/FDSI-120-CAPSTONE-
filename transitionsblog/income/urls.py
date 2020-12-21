
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
   
    path('income', views.index, name="income"),
    path('add_income', views.add_income, name="add_income"),
    path('edit_income/<int:id>', views.income_edit, name="income_edit"),
    path('income-delete/<int:id>', views.delete_income, name="delete_income"),
    path("search-income", csrf_exempt(views.search_income), name="search_income"),
    path('status', views.status_views, name="status"),

]
