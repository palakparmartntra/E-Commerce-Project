# Generated by Django 5.0.1 on 2024-01-19 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
