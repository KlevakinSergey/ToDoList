# Generated by Django 3.0.3 on 2020-02-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_auto_20200213_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.TextField(),
        ),
    ]
