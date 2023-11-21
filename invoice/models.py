from django.db import models
from django.urls import reverse
from dealer.models import Dealer

from transactions.models import ExportProduct, ImportProduct


################## import #############3
class ImportInvoice(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,blank=True,unique=False)
    description = models.TextField(unique=False,blank=True,null=True)
    date = models.DateField(unique=False)

    def total_yards(self):
        total_yards = 0
        details = ImportInvoiceDetail.objects.filter(invoice=self)
        for detail in details:
            total_yards += detail.import_product.yard
        return total_yards


    def __str__(self):
        return str(self.dealer)



class ImportInvoiceDetail(models.Model):
    invoice = models.ForeignKey(ImportInvoice, on_delete=models.CASCADE, blank=True, null=True, related_name='invoice_details',unique=False)
    import_product = models.ForeignKey(ImportProduct, on_delete=models.CASCADE, blank=True, null=True,unique=False) 

    def __str__(self):
        return f'المستخدم: {self.invoice.dealer.user} - التاجر : {self.invoice.dealer}'
 
   
################ Export ##################
class ExportInvoice(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,blank=True,unique=False)
    description = models.TextField(unique=False,blank=True,null=True)
    date = models.DateField(unique=False)
    
    def total_price(self):
        total = 0
        export_invoice_details = ExportInvoiceDetail.objects.filter(invoice=self)
        for detail in export_invoice_details:
            total += detail.export_product.total_price()
        return total
    def __str__(self):
        return str(self.dealer)
    
    


    
class ExportInvoiceDetail(models.Model):
    invoice = models.ForeignKey(ExportInvoice, on_delete=models.CASCADE, blank=True, null=True)
    export_product = models.ForeignKey(ExportProduct, on_delete=models.CASCADE,blank=True, null=True)
    def total_price(self):
            return self.export_product.quantity * self.export_product.price_of_one
    def __str__(self):
        return f'المستخدم: {self.invoice.dealer.user} - التاجر : {self.invoice.dealer}'
 