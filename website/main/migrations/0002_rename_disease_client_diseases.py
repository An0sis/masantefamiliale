# Generated by Django 4.2.11 on 2024-04-06 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='disease',
            new_name='diseases',
        ),
    ]
