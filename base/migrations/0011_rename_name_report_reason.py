# Generated by Django 4.1.3 on 2023-01-05 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20221223_1731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='name',
            new_name='reason',
        ),
    ]
