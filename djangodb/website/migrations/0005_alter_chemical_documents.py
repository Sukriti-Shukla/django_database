# Generated by Django 4.2.1 on 2023-05-18 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_chemical_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemical',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='docs/'),
        ),
    ]