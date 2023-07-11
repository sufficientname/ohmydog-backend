# Generated by Django 4.2.1 on 2023-07-11 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('CONSULTA_GENERAL', 'Consulta general'), ('VACUNACION_A', 'Vacunacion A'), ('VACUNACION_B', 'Vacunacion B'), ('DESPARASITACION', 'Desparasitacion'), ('CASTRACION', 'Castracion'), ('URGENCIA', 'Urgencia')], max_length=16)),
                ('date', models.DateField()),
                ('timeslot', models.CharField(choices=[('MANANA', 'Mañana'), ('TARDE', 'Tarde')], max_length=16)),
                ('hour', models.TimeField(null=True)),
                ('suggestion_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('PEN', 'Pendiente'), ('ACE', 'Aceptado'), ('REJ', 'Rechazado'), ('CAN', 'Cancelado'), ('COM', 'Completado')], default='PEN', max_length=16)),
                ('observations', models.TextField()),
                ('days_to_booster', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
            ],
        ),
    ]
