# Generated by Django 5.0.1 on 2024-02-23 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('products', '0004_alter_category_options_alter_brandproduct_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('section_type', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SectionItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='SectionSectionItemsThrough',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.section')),
                ('section_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.sectionitems')),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='section_items',
            field=models.ManyToManyField(through='products.SectionSectionItemsThrough', to='products.sectionitems'),
        ),
    ]