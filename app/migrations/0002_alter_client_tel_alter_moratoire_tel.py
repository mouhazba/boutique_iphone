# Generated by Django 4.1.7 on 2023-03-28 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='tel',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='moratoire',
            name='tel',
            field=models.CharField(max_length=120),
        ),
    ]
