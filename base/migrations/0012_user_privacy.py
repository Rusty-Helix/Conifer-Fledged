# Generated by Django 4.1.5 on 2023-01-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_rename_name_report_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='privacy',
            field=models.BooleanField(default=False),
        ),
    ]
