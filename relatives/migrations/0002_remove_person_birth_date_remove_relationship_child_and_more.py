# Generated by Django 5.1.4 on 2024-12-06 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relatives', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='child',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='relation_type',
        ),
        migrations.AddField(
            model_name='relationship',
            name='person',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='relatives.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parents', to='relatives.person'),
        ),
    ]