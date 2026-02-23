from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Collection
from django.db.models import Sum



# Create your views here.
def list(request):
    # get all collections from the database using pagination
    collections = Collection.objects.all()
    #  ned to build the following sql qurty
    # SELECT sum(amount), user_id, name  FROM drf_db.collection group by user_id ;
    collections = Collection.objects.values('user_id', 'name').annotate(total_amount=Sum('amount'))
    paginator = Paginator(collections, 10)  # Show 10 collections per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'collection/list.html', {'page_obj': page_obj})