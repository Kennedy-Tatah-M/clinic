# Generated by Django 5.0.1 on 2024-05-28 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0037_alter_doctor_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorDischargeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorId', models.PositiveIntegerField(null=True)),
                ('doctorName', models.CharField(max_length=40)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10)),
                ('age', models.IntegerField()),
                ('salary', models.PositiveIntegerField(blank=True)),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('problem', models.TextField(max_length=500, null=True)),
                ('admitDate', models.DateField(auto_now_add=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('releaseDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]