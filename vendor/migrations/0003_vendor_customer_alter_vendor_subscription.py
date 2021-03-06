# Generated by Django 4.0.3 on 2022-04-27 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0011_alter_invoice_charge_alter_invoice_customer_and_more'),
        ('vendor', '0002_alter_vendor_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.customer'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor', to='djstripe.subscription'),
        ),
    ]
