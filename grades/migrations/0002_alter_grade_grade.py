# Generated by Django 4.0.6 on 2022-08-15 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.IntegerField(choices=[(10, 'A'), (9, 'A-'), (8, 'B'), (7, 'B-'), (6, 'C'), (5, 'C-'), (4, 'D'), (3, 'D-'), (2, 'E'), (1, 'F')]),
        ),
    ]
