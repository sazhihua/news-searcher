# Generated by Django 3.2.16 on 2022-12-25 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articletype',
            name='site',
            field=models.CharField(max_length=36, null=True),
        ),
    ]
