# Generated by Django 4.1.5 on 2023-09-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datahub", "0054_usagepolicy_configs"),
    ]

    operations = [
        migrations.AddField(
            model_name="resourcefile",
            name="transcription",
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
        migrations.AddField(
            model_name="resourcefile",
            name="type",
            field=models.CharField(
                choices=[("youtube", "youtube"), ("pdf", "pdf")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="resourcefile",
            name="url",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="resourcefile",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="users/resources/"),
        ),
    ]
