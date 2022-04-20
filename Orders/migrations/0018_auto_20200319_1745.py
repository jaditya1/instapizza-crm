# Generated by Django 2.1.8 on 2020-03-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0017_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('0', 'Cash on Delivery'), ('1', 'Dineout'), ('2', 'Paytm'), ('3', 'Razorpay'), ('4', 'PayU'), ('5', 'EDC'), ('6', 'Mobiquik')], max_length=150, null=True, verbose_name='Payment Mode'),
        ),
    ]
