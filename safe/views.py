from django.shortcuts import render
from dealer.models import Dealer
from material.models import Material
from transactions.models import ExportProduct, DealerWithdraw
from decimal import Decimal
def index(request):
    safe = safe_calculate_totals()
    total_export_price = safe['total_export_price']
    total_withdrawals = safe['total_dealer_withdrawals']
    debt_or_credit = safe['debit_or_credit']
    total_materials = safe['total_dealer_materials']
    return render(request, 'index.html', {'total_export_price':total_export_price,'total_withdrawals':total_withdrawals,'debt_or_credit':debt_or_credit,'total_materials':total_materials})


def safe_calculate_totals():
    # Get all dealers
    dealers = Dealer.objects.all()
    
    total_dealer_withdrawals = Decimal(0)
    total_export_price = Decimal(0)
    total_dealer_materials = Decimal(0)
    
    for dealer in dealers:
        # Get withdrawals for the current dealer
        dealer_withdrawals = DealerWithdraw.objects.filter(dealer=dealer)
        total_dealer_withdrawals += sum(withdraw.withdraw for withdraw in dealer_withdrawals)
        dealer_materials = Material.objects.filter(dealer=dealer)
        
        # Get export products for the current dealer
        export_products = ExportProduct.objects.filter(product__dealer=dealer)
        total_export_price += sum(export_product.total_price() for export_product in export_products)
        total_dealer_materials += sum(material.price for material in dealer_materials)

    # Calculate the debit or credit for all dealers
    debit_or_credit = total_export_price - total_dealer_withdrawals - total_dealer_materials
    
    # Return the calculated values as a dictionary
    return {
        'total_dealer_withdrawals': total_dealer_withdrawals,
        'total_export_price': total_export_price,
        'debit_or_credit': debit_or_credit,
        'total_dealer_materials': total_dealer_materials
    }
