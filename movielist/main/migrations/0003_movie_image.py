# Generated by Django 3.1.4 on 2020-12-12 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201212_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.URLField(default=None, null=True),
        ),
    ]
