from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



departments=[('Orthodontics','Orthodontics'),
('Prosthodontics','Prosthodontics'),
('General dentist','General dentist'),
('Oral and maxillofacial surgery','Oral and maxillofacial surgery'),
('Endodontics','Endodontics'),
('Dentist','Dentist'),
('Staff','Staff')
]

expense_choice = [('Clinical Expense','Clinical Expense'),
                  ('Non-Clinic Expense','Non-Clinic Expense')]

sex = [('Male','Male'),
       ('Female','Female')]



class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    salary = models.PositiveIntegerField(null=False,blank=True)
    sex = models.CharField(max_length=10,null=False,choices=sex,default='Male')
    age = models.IntegerField(null=False,blank=False)
    mobile = models.CharField(max_length=20,null=True)
    department = models.CharField(max_length=50,choices=departments,default='General dentist')
    status=models.BooleanField(default=False)
    admitDate=models.DateField(auto_now_add=True)
    
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class DoctorDischargeDetails(models.Model):
    doctorId=models.PositiveIntegerField(null=True)
    doctorName=models.CharField(max_length=40)
    sex = models.CharField(max_length=10,null=False,choices=sex,default='Male')
    age = models.IntegerField(null=False,blank=False)
    salary = models.PositiveIntegerField(null=False,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)   
    department = models.CharField(max_length=50,choices=departments,default='General dentist')
    admitDate=models.DateField(auto_now_add=True)
    updateDate=models.DateField(auto_now=True)
    releaseDate=models.DateTimeField(auto_now=True,null=False)

    
    def __str__(self):
        return self.doctorName



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)  
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    sex = models.CharField(max_length=10,null=False,choices=sex,default='Male')
    age = models.IntegerField(null=False,blank=False)
    problem = models.TextField(max_length=500,null=False,blank=False)
    procedure = models.TextField(max_length=500,null=False,blank=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    consultation = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    newConsultation = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    amount = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    advance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    newAdvance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    balance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    medicineCost=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    newMedicineCost=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    total=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    newTotal=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    admitDate=models.DateField(auto_now_add=True)
    updateDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.problem+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now_add=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    sex = models.CharField(max_length=10,null=False,choices=sex,default='Male')
    age = models.IntegerField(null=False,blank=False)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    problem = models.TextField(max_length=500,null=True)
    procedure = models.TextField(max_length=500,null=False,blank=False)
    consultation = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    amount = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    newAdvance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    advance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    balance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    admitDate=models.DateField(auto_now_add=True)
    updateDate=models.DateField(auto_now=True)
    releaseDate=models.DateTimeField(auto_now=True,null=False)

    medicineCost=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    total=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)


class Income(models.Model):
    total_advance = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    total_medicineCost=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    total_OtherCharge=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    total=models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    incomeDate = models.DateField(auto_now_add=True)
    
    

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    type_expense = models.CharField(max_length=50,choices=expense_choice,default='Clinic Expense')
    amount = models.DecimalField(max_digits=20,decimal_places=0,null=False,blank=True)
    description = models.TextField(max_length=500)
    ExpenseDate = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.type_expense
    
class AdminSigup(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='admin_pic/images',null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    

    