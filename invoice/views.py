from django.forms import formset_factory
from django.shortcuts import redirect, render
from invoice.forms import ExInvoiceForm, ImInvoiceForm
from transactions.forms import ExportProductForm, ImportProductForm
from transactions.models import ExportProduct
from .models import ExportInvoice, ExportInvoiceDetail, ImportInvoice, ImportInvoiceDetail, ImportProduct
from django_htmx.http import HttpResponseClientRedirect
# Create your views here.
def add_edit_import_invoice(request):
    user = request.user
    ImportProductFormSet2 = formset_factory(ImportProductForm, extra=1)

    form = ImInvoiceForm(user,request.POST)
    formset = ImportProductFormSet2(request.POST, prefix='import_product')
    if request.method == "POST":
            if form.is_valid() and formset.is_valid():
                invoice = form.save()  # Save the invoice form
                
                import_product_list = []
                for product_form in formset:
                    if product_form.cleaned_data:  # Check if the form has valid data
                        import_product = product_form.save(commit=False)  # Create the import product object but don't save it yet
                        import_product.save()  # Save the import product object
                        import_product_list.append(import_product)
                
                # Link the imported products to the invoice

                for import_product in import_product_list:
                    ImportInvoiceDetail.objects.create(invoice=invoice, import_product=import_product)
                if request.htmx:
                    return HttpResponseClientRedirect("/invoice/list_import_invoice")
                return redirect("invoice:list_import_invoice")
    else:
        form = ImInvoiceForm(user)
        formset = ImportProductFormSet2(prefix='import_product')

    context = {
        "form": form,
        "formset": formset,
    }

    return render(request, "import_invoice/add_edit_import_invoice.html", context)

def add_edit_export_invoice(request):
    user = request.user
    ImportProductFormSet2 = formset_factory(ExportProductForm, extra=1)

    form = ExInvoiceForm(user,request.POST)
    formset = ImportProductFormSet2(request.POST, prefix='export_product')
    if request.method == "POST":
            if form.is_valid() and formset.is_valid():
                invoice = form.save()  # Save the invoice form
                
                export_product_list = []
                for product_form in formset:
                    if product_form.cleaned_data:  # Check if the form has valid data
                        export_product = product_form.save(commit=False)  # Create the import product object but don't save it yet
                        export_product.save()  # Save the import product object
                        export_product_list.append(export_product)
                
                # Link the imported products to the invoice
                for export_product in export_product_list:
                    ExportInvoiceDetail.objects.create(invoice=invoice, export_product=export_product)

                return redirect("invoice:view_invoice")
    else:
        form = ExInvoiceForm(user)
        formset = ImportProductFormSet2(prefix='export_product')

    context = {
        "form": form,
        "formset": formset,
    }

    return render(request, "export_invoice/add_edit_export_invoice.html", context)


def list_import_invoice(request): 
    total_product = ImportProduct.objects.count()
    total_invoice = ImportInvoice.objects.count()
    import_invoices = ImportInvoice.objects.all()
    context = {
        "total_product": total_product,
        "total_invoice": total_invoice,
        "import_invoices": import_invoices,
    }
    return render(request, "import_invoice/list_import_invoice.html", context)

def list_export_invoice(request): 
    total_product = ExportProduct.objects.count()
    total_invoice = ExportInvoice.objects.count()
    export_invoices = ExportInvoice.objects.all()
    context = {
        "total_product": total_product,
        "total_invoice": total_invoice,
        "export_invoices": export_invoices,
    }
    return render(request, "export_invoice/list_export_invoice.html", context)

def view_invoice_detail(request, import_id=None, export_id=None):
    if import_id:
        invoice = ImportInvoice.objects.get(id=import_id)
        invoice_detail = ImportInvoiceDetail.objects.filter(invoice=invoice)
        
    if export_id:
        invoice = ExportInvoice.objects.get(id=export_id)
        invoice_detail = ExportInvoiceDetail.objects.filter(invoice=invoice)

    context = {
        'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/invoice_detail.html", context)

