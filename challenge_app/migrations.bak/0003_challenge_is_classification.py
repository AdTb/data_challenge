# Generated by Django 3.0.4 on 2020-04-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_file', '0002_auto_20200414_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='is_classification',
            field=models.BooleanField(default=False),
        ),
    ]
