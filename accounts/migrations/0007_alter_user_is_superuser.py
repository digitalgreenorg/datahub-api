# Generated by Django 4.1.5 on 2024-09-03 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_created_at_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]