from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminUserSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model=models.AdminSigup
        fields=['profile_pic','email']



#for Doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','age','sex','salary','status','profile_pic']



#for Patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username']
        """ widgets = {
        'password': forms.PasswordInput()
        } """
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','problem','procedure','sex','age','consultation','newAdvance','amount','advance','balance','medicineCost']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class Income(forms.ModelForm):
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name", to_field_name="user_id")
    p_d_d_Id=forms.ModelChoiceField(queryset=models.PatientDischargeDetails.objects.all())
    
    class Meta:
        model= models.Patient
        fields = [
            'amount','advance','balance','medicineCost','consultation'
        ]        


class ExpenseUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username']
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model=models.Expense
        fields=['type_expense','amount','description','status']
        
    class ReportForm(forms.ModelForm):
        class Meta:
            model=models.Expense
            fields=['type_expense','amount','description']

        class Meta:
            model= models.Patient
            fields = [
                'amount','advance','balance','medicineCost','consultation'
            ]
        
class AskDateForm(forms.Form):
    fromDate=forms.DateField()
    toDate=forms.DateField()



