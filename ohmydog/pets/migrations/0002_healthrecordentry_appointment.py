# Generated by Django 4.2.1 on 2023-07-10 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthrecordentry',
            name='appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appointments.appointment'),
        ),
    ]