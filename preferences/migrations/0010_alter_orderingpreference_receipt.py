# Generated by Django 4.0.6 on 2022-08-15 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0001_initial'),
        ('preferences', '0009_alter_orderingpreference_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderingpreference',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.receipt'),
        ),
    ]