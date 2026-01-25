from django.shortcuts import render   
from django.http import HttpResponse
from .models import Loan

# Create your views here.
def view_loans(request):
    loans = Loan.objects.all()[:10]
    total_loans = Loan.objects.count()
    context = {
        'loans': loans,
        'total_loans': total_loans,
    }
    print("total_loans:", total_loans)
    return HttpResponse(f"Total Loans: {total_loans}")

def loan_dashboard(request):
    # limit 10 loans
    loans = Loan.objects.all()[:10]
    total_loans = Loan.objects.count()
    context = {
        'loans': loans,
        'total_loans': total_loans,
    }
    return render(request, 'loan/view_loans.html', context)