# Generated by Django 4.0.3 on 2022-05-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
