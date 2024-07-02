from django.shortcuts import render
from django.utils import timezone
from .models import MainBalance, Investment, Lend, UPIPayment, CreditCardPayment
from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from .models import MainBalance, Investment, Lend, UPIPayment, CreditCardPayment
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils import timezone
from .models import MainBalance, Investment, Lend, UPIPayment, CreditCardPayment
from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from .models import MainBalance, Investment, Lend, UPIPayment, CreditCardPayment
from datetime import datetime, timedelta

def dashboard(request):
    selected_month = int(request.GET.get('month', 0))  # Get selected month from query parameter

    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    if selected_month:
        start_of_selected_month = datetime(today.year, selected_month, 1).date()
        end_of_selected_month = start_of_selected_month.replace(month=start_of_selected_month.month % 12 + 1, day=1) - timedelta(days=1)
    else:
        start_of_selected_month = start_of_month
        end_of_selected_month = today

    # Calculate start and end dates for the previous month of selected month
    if start_of_selected_month.month == 1:  # If selected month is January, previous month is December of previous year
        start_of_previous_month = datetime(start_of_selected_month.year - 1, 12, 1).date()
        end_of_previous_month = datetime(start_of_selected_month.year - 1, 12, 1).date() + timedelta(days=31)
    else:
        start_of_previous_month = datetime(start_of_selected_month.year, start_of_selected_month.month - 1, 1).date()
        end_of_previous_month = start_of_previous_month.replace(month=start_of_previous_month.month % 12 + 1, day=1) - timedelta(days=1)

    # Query data from database for the selected month
    main_balance_selected_month = MainBalance.objects.filter(date__gte=start_of_selected_month, date__lte=end_of_selected_month)
    investments_selected_month = Investment.objects.filter(date__gte=start_of_selected_month, date__lte=end_of_selected_month)
    lends_selected_month = Lend.objects.filter(date__gte=start_of_selected_month, date__lte=end_of_selected_month)
    upi_payments_selected_month = UPIPayment.objects.filter(date__gte=start_of_selected_month, date__lte=end_of_selected_month)
    credit_card_payments_selected_month = CreditCardPayment.objects.filter(date__gte=start_of_selected_month, date__lte=end_of_selected_month)

    # Calculate totals for the selected month
    current_month_total = {
        'main_balance': sum(balance.amount for balance in main_balance_selected_month),
        'investments': sum(investment.amount for investment in investments_selected_month),
        'lends': sum(lend.amount for lend in lends_selected_month),
        'upi_payments': sum(payment.amount for payment in upi_payments_selected_month),
        'credit_card_payments': sum(payment.amount for payment in credit_card_payments_selected_month),
    }

    # Query data from database for the previous month of selected month
    main_balance_last_month = MainBalance.objects.filter(date__gte=start_of_previous_month, date__lte=end_of_previous_month)
    investments_last_month = Investment.objects.filter(date__gte=start_of_previous_month, date__lte=end_of_previous_month)
    lends_last_month = Lend.objects.filter(date__gte=start_of_previous_month, date__lte=end_of_previous_month)
    upi_payments_last_month = UPIPayment.objects.filter(date__gte=start_of_previous_month, date__lte=end_of_previous_month)
    credit_card_payments_last_month = CreditCardPayment.objects.filter(date__gte=start_of_previous_month, date__lte=end_of_previous_month)

    # Calculate totals for the last month of selected month
    last_month_total = {
        'main_balance': sum(balance.amount for balance in main_balance_last_month),
        'investments': sum(investment.amount for investment in investments_last_month),
        'lends': sum(lend.amount for lend in lends_last_month),
        'upi_payments': sum(payment.amount for payment in upi_payments_last_month),
        'credit_card_payments': sum(payment.amount for payment in credit_card_payments_last_month),
    }

    # Calculate differences between current month and last month
    difference_total = {
        'main_balance': current_month_total['main_balance'] - last_month_total['main_balance'],
        'investments': current_month_total['investments'] - last_month_total['investments'],
        'lends': current_month_total['lends'] - last_month_total['lends'],
        'upi_payments': current_month_total['upi_payments'] - last_month_total['upi_payments'],
        'credit_card_payments': current_month_total['credit_card_payments'] - last_month_total['credit_card_payments'],
    }

    # Fetch all investments for display in the list
    investments = Investment.objects.all()

    return render(request, 'dashboard.html', {
        'current_month_total': current_month_total,
        'last_month_total': last_month_total,
        'difference_total': difference_total,  # Pass difference values to template
        'investments': investments,
        'selected_month': selected_month,  # Pass selected month to template for display if needed
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import MainBalance, Investment, Lend, UPIPayment, CreditCardPayment
from .forms import InvestmentForm
from datetime import timedelta

def investment_list(request):
    investments = Investment.objects.all()
    return render(request, 'investment_list.html', {'investments': investments})

def investment_add(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investment_form.html', {'form': form})

def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            form.save()
            return redirect('investment_list')
    else:
        form = InvestmentForm(instance=investment)
    return render(request, 'investment_form.html', {'form': form})

def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == 'POST':
        investment.delete()
        return redirect('investment_list')
    return render(request, 'investment_confirm_delete.html', {'investment': investment})


