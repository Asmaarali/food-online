# Generated by Django 5.0.1 on 2024-05-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_1",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_2",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
