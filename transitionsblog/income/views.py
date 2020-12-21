from django.shortcuts import render, redirect
from .models import Source, Income
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
import json
from django.http import JsonResponse
import datetime

# Create your views here.

def search_income(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istarts_with=search_str, owner=request.user) | Income.objects.filter(
            date__istarts_with=search_str, owner=request.user) |Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter( 
            source__icontains=search_str, owner=request.user)   
        data = income.values()
        return JsonResponse(list(data), safe=False)



def index(request):
    categories = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator= Paginator(income, 2)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context={
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)



def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
             
        return render(request, 'income/add_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description required')
            return render(request, 'income/add_income.html', context)
        Income.objects.create(owner=request.user, amount=amount, date=date, 
                              source=source, description=description)  

        messages.success(request, 'Record saved!')  
        return redirect('income') 

        
def income_edit(request, id):
    income =  Income.objects.get(pk=id)
    sources = Source.objects.all()
    context={
        ' income': income,
        'values':  income,
        'sources': sources,
    }
    if request.method =='GET':
       
        return render(request, 'income/edit_income.html', context)
    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'No amount, No cake!')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'No description, No cake!')
            return render(request, 'income/edit_income.html', context)
      
        income.amount=amount
        income.date=date
        income.source=source
        income.description=description   
        income.save()                      
        messages.success(request, 'Record Updated, YaY cake')  
        return redirect('income')

      
def delete_income(request, id):
    income= Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Where did the Cake go, you deleted it.')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    income = Income.objects.filter(owner=request.user,
        date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_source(income):
        return income.source
    source_list = list(set (map(get_source, income))) 

    def get_income_source_amount(source):
        amount=0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for x in income:
        for y in source_list:
            finalrep[y]=get_income_source_amount(y)
    return JsonResponse({'income_source_data': finalrep}, safe=False) 

def status_views(request):
    return render(request, 'income/status.html')   



