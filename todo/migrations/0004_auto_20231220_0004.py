# Generated by Django 2.2.24 on 2023-12-20 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20231220_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Labels'),
        ),
    ]
