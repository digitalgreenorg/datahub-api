# Generated by Django 4.1.5 on 2023-08-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datahub", "0046_datasetv2file_connection_details_datasetv2filereload"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasetv2file",
            name="connection_details",
            field=models.JSONField(default=dict, null=True),
        ),
    ]
