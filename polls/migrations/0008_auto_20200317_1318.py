# Generated by Django 3.0.3 on 2020-03-17 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20200317_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Neighborhood'),
        ),
    ]
