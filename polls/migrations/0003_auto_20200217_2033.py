# Generated by Django 3.0.3 on 2020-02-17 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200217_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='detail_text',
            field=models.TextField(blank=True, null=True, verbose_name='Details zur Frage'),
        ),
    ]