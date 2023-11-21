# Generated by Django 4.1.3 on 2023-11-20 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_importinvoicedetail_import_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exportinvoicedetail',
            name='export_product',
        ),
        migrations.RemoveField(
            model_name='exportinvoicedetail',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='importinvoicedetail',
            name='import_product',
        ),
        migrations.RemoveField(
            model_name='importinvoicedetail',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='dealer',
        ),
        migrations.DeleteModel(
            name='ExportInvoice',
        ),
        migrations.DeleteModel(
            name='ImportInvoice',
        ),
        migrations.DeleteModel(
            name='ExportInvoiceDetail',
        ),
        migrations.DeleteModel(
            name='ImportInvoiceDetail',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]