from django.shortcuts import redirect, render,get_object_or_404
from dealer.views import calculate_totals
from dealer.models import Dealer
from .forms import MaterialForm
from .models import Material
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
# Create your views here.
def material(request):
    current_user = request.user.profile
    materials = Material.objects.filter(user=current_user)
    return render(request, 'material.html', {'materials':materials})


def add_edit_dealer_material(request, material_id=None):
    if material_id:
        # Edit mode
        material_instance = get_object_or_404(Material, pk=material_id)
        form = MaterialForm(request.POST or None, instance=material_instance)
    else:
        # Add mode
        form = MaterialForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حفظ معلومات العميل بنجاح')
            return redirect('material:material')

    return render(request, 'add_edit_material.html', {'form': form})


def delete_material(request, id ):
    material =get_object_or_404(Material, id=id)
    if request.method == 'POST':
        material.delete()
        messages.success(request,'تم حذف المنتج بنجاح')
        return redirect('material:material')
    return render(request, 'delete_material.html')


def material_by_dealer(request, dealer_id):
    current_user = request.user.profile
    dealers = Dealer.objects.filter(user=current_user)
    dealer = get_object_or_404(Dealer, id=dealer_id)
    materials = Material.objects.filter(dealer__in=dealers).filter(dealer=dealer)
    dealer_totals = calculate_totals(dealer_id)
    total_materials = dealer_totals['total_dealer_materials']
    
    return render(request, 'material_by_dealer.html', {'materials': materials,'dealer':dealer,'total_materials':total_materials})

def generate_pdf_dealer_materail(request,  dealer_id):

       dealer = get_object_or_404(Dealer, id=dealer_id)
       materials = Material.objects.filter(dealer=dealer)
       dealer_totals = calculate_totals(dealer_id)
       total_materials = dealer_totals['total_dealer_materials']
       template = get_template('pdf_template.html')
       context = {'materials': materials,
                  'dealer': dealer,
                  'total_materials':total_materials}
       html_string = template.render(context)
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="dealer_material_pdf_filename.pdf"'
       return response
   