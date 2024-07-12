# Generated by Django 5.0.1 on 2024-04-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0019_income_remove_patient_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='admitDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='salary',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='ExpenseDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='incomeDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='total_OtherCharge',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='total_advance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='total_medicineCost',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='admitDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='advance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='consultation',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='medicineCost',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='newAdvance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='updateDate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='admitDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='advance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='consultation',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='medicineCost',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='newAdvance',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='releaseDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='patientdischargedetails',
            name='updateDate',
            field=models.DateField(auto_now=True),
        ),
    ]
