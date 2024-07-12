# Generated by Django 5.0.1 on 2024-05-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0038_doctordischargedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordischargedetails',
            name='department',
            field=models.CharField(choices=[('Orthodontics', 'Orthodontics'), ('Prosthodontics', 'Prosthodontics'), ('General dentist', 'General dentist'), ('Oral and maxillofacial surgery', 'Oral and maxillofacial surgery'), ('Endodontics', 'Endodontics'), ('Dentist', 'Dentist'), ('Staff', 'Staff')], default='General dentist', max_length=50),
        ),
    ]