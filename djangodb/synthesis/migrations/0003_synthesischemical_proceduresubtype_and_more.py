# Generated by Django 4.2.1 on 2023-06-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthesis', '0002_alter_synthesischemical_added_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='synthesischemical',
            name='proceduresubtype',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='synthesischemical',
            name='proceduretype',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]