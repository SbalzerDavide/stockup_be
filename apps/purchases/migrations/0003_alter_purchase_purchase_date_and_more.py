# Generated by Django 5.1.7 on 2025-06-02 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchases", "0002_alter_purchase_shopping_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="purchase_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="total_items",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
