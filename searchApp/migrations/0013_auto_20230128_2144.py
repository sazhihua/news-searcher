# Generated by Django 3.2.16 on 2023-01-28 21:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('searchApp', '0012_auto_20230128_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.CharField(default=uuid.UUID('61ec8934-cd1e-4ef4-af92-9366484ee3a2'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='articletype',
            name='id',
            field=models.CharField(default=uuid.UUID('adfebffa-8328-49bb-9a21-5c389e08efe7'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='documentprocess',
            name='id',
            field=models.CharField(default=uuid.UUID('ee391647-c9f9-4dcd-8f86-627bfd0b2960'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='patchlog',
            name='id',
            field=models.CharField(default=uuid.UUID('a52c1eb3-3829-453f-8511-b9f7c9b3988d'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='searchlog',
            name='id',
            field=models.CharField(default=uuid.UUID('c664fe33-4eee-4872-af3c-4d6a4c9709c8'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='searchlog',
            name='mobileflag',
            field=models.CharField(choices=[('1', '是'), ('0', '否')], max_length=1, null=True, verbose_name='移动端标识'),
        ),
        migrations.AlterField(
            model_name='sourcesite',
            name='id',
            field=models.CharField(default=uuid.UUID('58574981-e9bd-4ea1-9031-1fc06031bb03'), max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
