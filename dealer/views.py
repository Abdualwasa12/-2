from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from invoice.models import ExportInvoiceDetail
from material.models import Material

from transactions.models import DealerWithdraw, ExportProduct
from .models import Dealer
from django.contrib import messages
from .forms import DealerForm

# Create your views here.


def dealer(request):
    current_user = request.user.profile
    dealers = Dealer.objects.filter(user=current_user)
    return render(request, 'list_dealer.html', {'dealers':dealers})





def add_edit_dealer(request, dealer_id=None):
    if dealer_id:
        # Edit mode
        dealer_instance = get_object_or_404(Dealer, pk=dealer_id, user=request.user.profile)
        form = DealerForm(request.POST or None, instance=dealer_instance)
    else:
        # Add mode
        form = DealerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_user= form.save(commit=False)
            current_user.user = request.user.profile
            current_user.save()
            messages.success(request, 'تم حفظ معلومات العميل بنجاح')
            return redirect('dealer:list_dealer')
    return render(request, 'add_edit_dealer.html', {'form': form})



def delete_dealer(request, id ):
    
    dealer =get_object_or_404(Dealer, id=id)
    if dealer.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this hoooo")
    if request.method == 'POST':
        dealer.delete()

        messages.success(request,'تم حذف العميل بنجاح')
        return redirect('dealer:list_dealer')
    return render(request, 'delete_dealer.html')




def detail_dealer(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id, user=request.user.profile)
    dealer_totals =calculate_totals(dealer_id)
    

    total_export_price = dealer_totals['total_export_price']
    debit_or_credit = dealer_totals['debit_or_credit']
    total_withdrawals_materails = dealer_totals['total_withdrawals_materails']
        
    return render(request, 'detail_dealer.html', {'dealer': dealer,
                                                  'total_export_price':total_export_price,
                                                  'debit_or_credit':debit_or_credit,
                                                  'total_withdrawals_materails':total_withdrawals_materails
                                                  
                                                  })



def calculate_totals(id):
     ######## Dealer #########
    dealer = get_object_or_404(Dealer, id=id)
    dealer_withdrawals = DealerWithdraw.objects.filter(dealer=dealer)
    dealer_materials = Material.objects.filter(dealer=dealer)
 
    total_dealer_withdrawals = sum(withdraw.withdraw for withdraw in dealer_withdrawals)
    total_dealer_materials = sum(material.price for material in dealer_materials)
    
    # Get all export products for the dealer
    export_products = ExportInvoiceDetail.objects.filter(invoice__dealer=dealer)
    # Calculate the total price in Python

    total_withdrawals_materails = total_dealer_materials + total_dealer_withdrawals
    total_export_price = sum(export_product.total_price() for export_product in export_products)
    debit_or_credit = total_export_price - total_dealer_withdrawals - total_dealer_materials
     # Return the calculated values as a dictionary
    return {

        'total_dealer_withdrawals':total_dealer_withdrawals,
        'total_export_price':total_export_price,
        'debit_or_credit':debit_or_credit,
        'total_dealer_materials':total_dealer_materials,
        'total_withdrawals_materails':total_withdrawals_materails
        
    }