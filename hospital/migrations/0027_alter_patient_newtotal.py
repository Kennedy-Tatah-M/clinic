# Generated by Django 5.0.1 on 2024-04-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0026_patient_newtotal_alter_patient_newconsultation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='newTotal',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
    ]