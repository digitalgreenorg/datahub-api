# Generated by Django 4.1.5 on 2023-08-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datahub', '0042_alter_usagepolicy_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usagepolicy',
            name='api_key',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
