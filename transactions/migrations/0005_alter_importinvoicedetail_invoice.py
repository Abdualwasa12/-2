# Generated by Django 4.1.3 on 2023-11-20 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_importinvoicedetail_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importinvoicedetail',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='transactions.importinvoice'),
        ),
    ]
