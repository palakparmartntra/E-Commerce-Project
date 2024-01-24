# Generated by Django 5.0.1 on 2024-01-24 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_address_phone_no_alter_address_zipcode_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='reciever_name',
            new_name='receiver_name',
        ),
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(blank=True, null=True),
        ),
    ]
