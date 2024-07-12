from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages




# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    form=forms.AdminUserSigupForm()
    adminForm=forms.AdminSignupForm()
    my_dic = {'form':form,'adminForm':adminForm}
    if request.method=='POST':
        form=forms.AdminUserSigupForm(request.POST)
        adminForm=forms.AdminSignupForm(request.POST, request.FILES)
        
        if form.is_valid() and adminForm.is_valid():
            admincount = models.AdminSigup.objects.all().count()
            admin = models.AdminSigup.objects.all()
            if admincount <= 2:
                user=form.save()
                user.set_password(user.password)
                user.save()
                admin=adminForm.save(commit=False)
                admin.user=user
                admin.status=True
            
                admin=admin.save()
                my_admin_group = Group.objects.get_or_create(name='ADMIN')
                my_admin_group[0].user_set.add(user)
                messages.success(request,"Admin created successfully." )
                return HttpResponseRedirect('adminlogin')
            else:
                messages.warning(request,"The number of Admins can not be more than 3." )
                return redirect('')
            #return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',context=my_dic)




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            doctorcount = models.Doctor.objects.all().filter(status=True).count()
            
            if doctorcount < 2 :
                user=userForm.save()
                user.set_password(user.password)
                user.save()

                doctor=doctorForm.save(commit=False)
                doctor.user=user
                doctor.status=True
                doctor.save()

                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
            
                messages.success(request,"Staff created "+doctor.get_name+ " successfully." )
                return HttpResponseRedirect('doctorlogin')
            else:
                messages.warning(request,"The number of Staff can not be more than 1." )
                return redirect('')
        #return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            #user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.newAdvance = patient.advance
            patient.balance = int(patient.amount)- int(patient.advance)        
            patient.total = int(patient.advance)+int(patient.medicineCost)+int(patient.consultation)        
            if int(patient.amount)- int(patient.advance) < 0:
                messages.warning(request,"Advance can not be more than the amount to be paid..")
                return render(request,'hospital/admin_add_patient.html',context=mydict)
            
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request,"Patient " +patient.get_name+ " added successfully")
        return HttpResponseRedirect('admin-view-patient')
    mydict={'userForm':userForm,'patientForm':patientForm}
    return render(request,'hospital/admin_add_patient.html',context=mydict)




#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    
    if is_admin(request.user):
        return redirect('admin-dashboard')
        
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')





#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id') #getting the last doctor input
    
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    total = 0
    total = models.Patient.objects.filter(status=True).aggregate(Sum('total'))['total__sum']
    print(total)
    expense = models.Expense.objects.all().filter(status=True)
    admin = models.AdminSigup.objects.get(user_id=request.user.id), #for profile picture of admin in sidebar
    for i in admin:
        pass
        #print(i.profile_pic.url)
    #print(admin.img.url)
    amount = 0
    for expense in expense:
        amount += expense.amount 
    print(amount)
    sum = 0
    sum = int(total) - int(amount)
    if sum == 0:
        messages.success(request,"No profit made")
    elif sum < 0:
        messages.warning(request,"You made a loss of F CFA :")
    else:
        messages.success(request,"You made a profit of F CFA : ")
    
    mydict={
        'expense':expense,
        'amount':amount,
        'total':total,
        'sum':sum,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'admin':admin,
    }
    
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True).order_by('-id')
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        doctors = models.Doctor.objects.filter(status=True).raw('select * from hospital_doctor where admitDate between "'+fromDate+'" and "'+toDate+'"') 
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})
            

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    messages.warning(request,"Doctor "+doctor.get_name+ " deleted successfully.")
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            messages.success(request,"Doctor "+doctor.get_name+ " updated Successfully.")
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.success(request,"Doctor " +doctor.get_name+ " added successfully." )
        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    #messages.success(request,"Admin has approved Doctor successfully.")
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    messages.warning(request,"Doctor "+doctor.get_name+ " rejected successfully.")
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patient=models.Patient.objects.all().filter(status=True).order_by('-id')
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        patients = models.Patient.objects.filter(status=True).raw('select * from hospital_patient where admitDate between "'+fromDate+'" and "'+toDate+'"') 
        return render(request,'hospital/admin_view_patient.html',{'patients':patients})
    return render(request,'hospital/admin_view_patient.html',{'patients':patient})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    messages.warning(request,"Patient "+patient.get_name+ " deleted successfully.")
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    advance = patient.advance
    balance = patient.balance
    medicineCost = patient.medicineCost
    consultation = patient.consultation
    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(instance=patient)
    print(patient.updateDate)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            #user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            #patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            #patient.admitDate = patient.updateDate
            patient.newAdvance = int(patient.advance)
            patient.newMedicineCost = patient.medicineCost
            patient.newConsultation = patient.consultation
            advance1 = advance + int(patient.advance)  
            patient.balance = int(patient.amount) - int(advance1)
            if patient.balance <0:
                messages.warning(request,"Advance can not be more than the amount to be paid..")
                return redirect('update-patient',patient.id)
            patient.advance = int(advance1)
            
            patient.total = int(patient.advance)+int(medicineCost+patient.medicineCost)+int(consultation+patient.consultation)      
              
            patient.medicineCost = int(medicineCost+patient.medicineCost)
            patient.consultation = int(consultation+patient.consultation)
            patient.newTotal = int(patient.newAdvance)+int(patient.newMedicineCost)+int(patient.newConsultation) 
            patient.save()
            if int(patient.balance) == 0:
                messages.info(request,"Patient " +patient.get_name+ " updated successfully.\n" " You completed your bill, thanks..")
                return redirect('admin-view-patient')
            messages.success(request,"Patient "+patient.get_name+ " updated succesfully.")
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            #user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
             
            patient.newAdvance = patient.advance
            patient.newMedicineCost = patient.medicineCost
            patient.newConsultation = patient.consultation
            patient.balance = int(patient.amount)- int(patient.advance)        
            patient.total = int(patient.advance)+int(patient.medicineCost)+int(patient.consultation) 
            patient.newTotal = int(patient.newAdvance)+int(patient.newMedicineCost)+int(patient.newConsultation)        
            if int(patient.amount)- int(patient.advance) < 0:
                messages.warning(request,"Advance can not be more than the amount to be paid..")
                return render(request,'hospital/admin_add_patient.html',context=mydict)
            
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            if int(patient.balance) == 0:
                messages.info(request,"Patient " +patient.get_name+ " added successfully" " You completed your bill, thanks..")
                return HttpResponseRedirect('admin-view-patient')
            messages.success(request,"Patient " +patient.get_name+ " added successfully")
        return HttpResponseRedirect('admin-view-patient')
    mydict={'userForm':userForm,'patientForm':patientForm}
    return render(request,'hospital/admin_add_patient.html',context=mydict)






#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_doctor.html',{'doctors':doctors})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
     # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'sex':patient.sex,
        'age':patient.age,
        'mobile':patient.mobile,
        'address':patient.address,
        'problem':patient.problem,
        'procedure':patient.procedure,
        'consultation':patient.consultation,
        'amount':patient.amount,
        'advance':patient.advance,
        'newAdvance':patient.newAdvance,
        'balance':patient.balance,
        'medicineCost':patient.medicineCost,
        'admitDate':patient.admitDate,
        'todayDate':datetime.now(),
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'consultation':patient.consultation,
            'amount':patient.amount,
            'advance':patient.advance,
            'newAdvance':patient.newAdvance,
            'balance':patient.balance,
            'medicineCost':patient.medicineCost,
            'total':int(patient.advance)+int(patient.medicineCost)+int(patient.consultation)
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.sex=patient.sex
        pDD.age=patient.age
        pDD.problem=patient.problem
        pDD.procedure=patient.procedure
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.consultation=patient.consultation
        pDD.amount=patient.amount
        pDD.advance=patient.advance
        pDD.newAdvance=patient.newAdvance
        pDD.balance=patient.balance
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=datetime.now()
        pDD.medicineCost=patient.medicineCost
        pDD.amount=patient.amount
        pDD.advance=patient.advance
        pDD.balance=int(patient.amount) - int(patient.advance)
        pDD.total=int(patient.advance)+int(patient.medicineCost)+int(patient.consultation)
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_doctor_view(request,pk):
    patient=models.Doctor.objects.get(id=pk)
    total = 0
    total = models.Expense.objects.filter(description=patient.get_name).aggregate(Sum('amount'))['amount__sum'] 
     
    #print(total)
    
     # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'sex':patient.sex,
        'age':patient.age,
        'mobile':patient.mobile,
        'address':patient.address,
        'salary':patient.salary,
        'department':patient.department,
        'total':total,
        'admittedDate':patient.admitDate,
        'todayDate':datetime.now(),
    }
    if request.method == 'POST':
        feeDict ={
            'salary':patient.salary,
            'todayDate':datetime.now(),            
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.DoctorDischargeDetails()
        pDD.doctorId=pk
        pDD.doctorName=patient.get_name
        pDD.sex=patient.sex
        pDD.age=patient.age
        pDD.salary=patient.salary
        pDD.department=patient.department
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=datetime.now()
      
        pDD.save()
        return render(request,'hospital/doctor_final_bill.html',context=patientDict)
    return render(request,'hospital/doctor_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'sex':dischargeDetails[0].sex,
        'age':dischargeDetails[0].age,
        'mobile':dischargeDetails[0].mobile,
        'problem':dischargeDetails[0].problem,
        'procedure':dischargeDetails[0].procedure,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'medicineCost':dischargeDetails[0].medicineCost,
        'amount':dischargeDetails[0].amount,
        'advance':dischargeDetails[0].advance,
        'newAdvance':dischargeDetails[0].newAdvance,
        'balance':dischargeDetails[0].balance,
        'consultation':dischargeDetails[0].consultation,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)


def download_doctor_pdf_view(request,pk):
    dischargeDetails=models.DoctorDischargeDetails.objects.all().filter(doctorId=pk).order_by('-id')[:1]
    doc=models.Doctor.objects.get(id=pk)
    total = 0
    total = models.Expense.objects.filter(description=dischargeDetails[0].doctorName).aggregate(Sum('amount'))['amount__sum'] 
    #print(total)
    dict={
        'name':dischargeDetails[0].doctorName,
        
        'address':dischargeDetails[0].address,
        'sex':dischargeDetails[0].sex,
        'age':dischargeDetails[0].age,
        'mobile':dischargeDetails[0].mobile,
        'department':dischargeDetails[0].department,       
        'admitDate':doc.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        
        'salary':dischargeDetails[0].salary,
        
        'total':total,
    }
    return render_to_pdf('hospital/download_doctor.bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        appointments = models.Appointment.objects.raw('select * from hospital_appointment where appointmentDate between "'+fromDate+'" and "'+toDate+'"') 
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
            messages.success(request,"Appointment added successfully.")
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    messages.success(request,"Appointment approved successfully.")
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    messages.warning(request,"Appointment rejected successfully.")
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_add_patient(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.newAdvance = patient.advance
            patient.newMedicineCost = patient.medicineCost
            patient.newConsultation = patient.consultation
            patient.balance = int(patient.amount)- int(patient.advance)        
            patient.total = int(patient.advance)+int(patient.medicineCost)+int(patient.consultation)        
            patient.newTotal = int(patient.newAdvance)+int(patient.newMedicineCost)+int(patient.newConsultation)        
            if int(patient.amount)- int(patient.advance) < 0:
                messages.warning(request,"Advance can not be more than the amount to be paid..")
                return render(request,'hospital/doctor_add_patient.html',context=mydict)
            
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request,"Patient " +patient.get_name+ " added successfully")
            mydict={'userForm':userForm,'patientForm':patientForm}
            return redirect('doctor-patient')
    mydict={'userForm':userForm,'patientForm':patientForm}
    return render(request,'hospital/doctor_add_patient.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    advance = patient.advance
    balance = patient.balance
    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.newAdvance = int(patient.advance)
            advance1 = advance + int(patient.advance)  
            patient.balance = int(patient.amount) - int(advance1)
            if patient.balance <0:
                messages.warning(request,"Advance can not be more than the amount to be paid..")
                return redirect('update-patient',patient.id)
            patient.advance = int(advance1)
            
            patient.total = int(patient.advance)+int(patient.medicineCost)+int(patient.consultation)        
            
            patient.save()
            messages.success(request,"Patient "+patient.get_name+ " updated succesfully.")
            return redirect('doctor-view-patient')
    return render(request,'hospital/doctor_update_patient.html',context=mydict)






@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctoginr_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(problem__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def search_view1(request):
    #searching for patient
    #doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True).filter(Q(problem__icontains=query)|Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query))
    """ return render(request,'hospital/admin_view_patient.html',{'patients':patients}) """

    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def search_doctor(request):
    #doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)|Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query))
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'problem':patient.problem,
    'procedure':patient.procedure,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'sex':patient.sex,
        'age':patient.age,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'problem':patient.problem,
        'procedure':patient.procedure,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'consultation':dischargeDetails[0].consultation,
        'advance':dischargeDetails[0].advance,
        'newAdvance':dischargeDetails[0].newAdvance,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_revenu(request):
    total = 0
    total = models.Patient.objects.filter(status=True).aggregate(Sum('total'))['total__sum']        
    
    return render(request,'hospital/admin_revenu.html',{
        'total':total
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_revenu_view(request):
    form = forms.PatientForm(request.POST) 
    total = 0 
    new_medicineCost =0
    new_consultation =0
    new_total =0 
    treatment_income = 0
    total_medicineCost = 0
    total_othercharge = 0 
    advance2 = 0
    if request.method == 'POST':
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if patientForm.is_valid():
            patient=patientForm.save(commit=False)
            advance2 = patient.newAdvance
            print(advance2)
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')               
        patient = models.Patient.objects.all().filter(status=True).raw('select * from hospital_patient where admitDate between "'+fromDate+'" and "'+toDate+'"') 
        data = forms.Income(request.POST)
        for i in patient:
            total += i.newTotal
            treatment_income += i.newAdvance
            total_medicineCost += i.newMedicineCost
            total_othercharge += i.newConsultation
        my_dic = {'patient':patient,
                  'total':total,
                  'treatment_income':treatment_income,
                  'total_medicineCost':total_medicineCost,
                  'total_othercharge':total_othercharge
        } 
        return render(request,'hospital/admin_view_revenu.html',context=my_dic)
    else:
        patient = models.Patient.objects.all().filter(status=True)  
        #total = models.Patient.objects.filter(status=True).aggregate(Sum('total'))['total__sum'] 
        total_advance = models.Patient.objects.filter(status=True).aggregate(Sum('newAdvance'))['newAdvance__sum'] 
        total_medicineCost = models.Patient.objects.filter(status=True).aggregate(Sum('newMedicineCost'))['newMedicineCost__sum']
        total_othercharge = models.Patient.objects.filter(status=True).aggregate(Sum('newConsultation'))['newConsultation__sum']
        total = int(total_advance)+ int(total_medicineCost)+int(total_othercharge)
        for i in patient:
            patient.newTotal = i.newTotal
        my_dic = {'patient':patient,
              'total':total,
              'total_medicineCost':total_medicineCost,
              'total_advance':total_advance,
              'total_othercharge':total_othercharge}
        income = models.Income(total_advance=total_advance,total_medicineCost=total_medicineCost,total_OtherCharge=total_othercharge,
        total=total) 
        #income.save()  
    return render(request,'hospital/admin_view_revenu.html',context=my_dic)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_revenu_generate_report(request):
    total = 0  
    new_advance = 0
    new_medicine = 0 
    treatment_income =0
    new_consultation = 0
    total_advance = 0
    treatment_income = 0
    total_medicineCost = 0
    total_othercharge = 0 
    incomeDate = date.today()
    if request.method == 'POST':  
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')               
        patient = models.Patient.objects.all().filter(status=True).raw('select * from hospital_patient where updateDate between "'+fromDate+'" and "'+toDate+'"') 
        
        for i in patient:
            #incomeDate = i.admitDate
            total += i.newTotal
            treatment_income += i.newAdvance
            total_medicineCost += i.newMedicineCost
            total_othercharge += i.newConsultation
            
        my_dic = {'patient':patient,
                  'total':total,
                  'total_advance':treatment_income,
                  'total_medicineCost':total_medicineCost,
                  'total_othercharge':total_othercharge,
                  'incomeDate':incomeDate
        }
        income = models.Income(total_advance=treatment_income,total_medicineCost=total_medicineCost,total_OtherCharge=total_othercharge,total=total) 
        income.save()   
        return render_to_pdf('hospital/download_revenu_report.html',my_dic)
   
    
def download_pdf_revenu_report(request):
    return render_to_pdf('hospital/download_revenu_report.html')
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_expense(request):
    expense = models.Expense.objects.all().filter(status=True)
    total = 0
    for i in expense:
        total += i.amount
    return render(request, 'hospital/admin_expense_dashboard.html',{'total':total})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_expense12(request):   
    user = models.Expense.objects.filter(user_id=request.user.id)       
    expense = models.Expense.objects.all().filter(status=True).order_by('-id') 
    my_dic = {
                    'expense':expense,
                    'user':user,
                }     
    return render(request, 'hospital/admin_view_expense.html',context=my_dic)

            


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_expense_generate_report(request):
    expenseDate = date.today()
    expenseDateTime = datetime.now()
    user = models.Expense.objects.filter(user_id=request.user.id)
    total_expense = 0
    expenseDate =datetime.now()
    
    query = request.POST['query']
    
    expense1=models.Expense.objects.all().filter(status=True).filter(Q(type_expense__icontains=query)|Q(user__username__icontains=query)|Q(description__icontains=query))
    for r in expense1:
        #total_expense += r.amount
        pass
    exp = r.description
    print(exp) 

    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        
        expense = models.Expense.objects.filter(Q (status=True) & Q(Q(ExpenseDate__gte=fromDate) & Q(ExpenseDate__lte=toDate)) & Q(description=exp)) 
        
        for i in expense:
            total_expense += i.amount
          
        #print(i.description)
        #print(i.status) 
        my_dic = {
                    'expense':expense,
                    'user':user,
                    'expenseDateTime':expenseDateTime,
                    'total_expense':total_expense,               
                    }
                
        return render_to_pdf('hospital/download_expense_report.html',my_dic)        
    



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def download_pdf_expense_report(request):
    user = models.Expense.objects.filter(user_id=request.user.id)
    expense = models.Expense.objects.all()
    form = forms.ExpenseForm(request.POST)
    
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        expense = models.Expense.objects.filter(status=True).raw('select * from hospital_expense where ExpenseDate between "'+fromDate+'" and "'+toDate+'"') 
        
        expense_type = form['type_expense']
        amount = form['amount']     
        description = form['description']
        
        for i in expense:
             expenseDate = i.ExpenseDate       
        my_dic = {
            'expense':expense,
            'user':user,
            'expense_type':expense_type,
            'amount':amount,
            'description':description,
            'expenseDate':expenseDate,
            }
        return render_to_pdf('hospital/download_expense_report.html',my_dic)
        
    else:
         user = models.Expense.objects.filter(user_id=request.user.id)
         expense = models.Expense.objects.all()
         for i in expense:
             expenseDate = i.ExpenseDate 
         my_dic = {
             'user':user,
             'expense':expense,
             'expenseDate':expenseDate,            
         }     
    return render_to_pdf('hospital/download_expense_report.html',my_dic)
    

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_expense(request):
    expense = models.Expense.objects.all().filter(status=True)
    total = 0
    for i in expense:
        total += i.amount
    my_dic = {
        'doctor':models.Doctor.objects.get(user_id=request.user.id),
        'total':total
    }
    return render(request, 'hospital/doctor_expense_dashboard.html',my_dic)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_expense(request):   
    user = models.Expense.objects.filter(user_id=request.user.id)
    expense = models.Expense.objects.all().filter(status=True)
    form = forms.ExpenseForm(request.POST)
    total_expense = 0
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')  
        toDate = request.POST.get('toDate')
        expense = models.Expense.objects.filter(status=True).raw('select * from hospital_expense where ExpenseDate between "'+fromDate+'" and "'+toDate+'"') 
        expense_type = form['type_expense']
        amount = form['amount']     
        description = form['description'] 
        for i in expense:
            total_expense += i.amount            
        my_dic = {
                    'expense':expense,
                    'user':user,
                    'expense_type':expense_type,
                    'amount':total_expense,
                    'description':description,                   
                    }
        return render(request, 'hospital/doctor_view_expense_view.html',context=my_dic)       
    else:
        user = models.Expense.objects.filter(user_id=request.user.id)
        expense = models.Expense.objects.all().filter(status=True) 
        for i in expense:
            expenseDate = i.ExpenseDate
        my_dic = {
                    'expense':expense,
                    'user':user,
                    'expenseDate':expenseDate
                }     
    return render(request, 'hospital/doctor_view_expense_view.html',context=my_dic)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_expense(request):
    userForm = forms.ExpenseUserForm()
    expenseForm = forms.ExpenseForm()
    if request.method=='POST':
        userForm=forms.ExpenseUserForm(request.POST)
        expenseForm=forms.ExpenseForm(request.POST)
        if expenseForm.is_valid():            
            expense=expenseForm.save(commit=False)
            expense.user_id = request.user.id
            expense.status = True
            expense.save()
            messages.success(request,'Expense added successfully.')
        return HttpResponseRedirect('admin-expense-view')
    
    mydict={'userForm':userForm,'expenseForm':expenseForm,
    }
    return render(request, 'hospital/admin_add_expense.html',context=mydict)

            

            


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_expense(request):
    userForm = forms.ExpenseUserForm()
    expenseForm = forms.ExpenseForm()
    if request.method=='POST':
        userForm=forms.ExpenseUserForm(request.POST)
        expenseForm=forms.ExpenseForm(request.POST)
        if expenseForm.is_valid():            
            expense=expenseForm.save(commit=False)
            expense.user_id = request.user.id
            expense.save()
            messages.success(request,'Expense added successfully.')
        return HttpResponseRedirect('doctor-add-expense')
    mydict={'userForm':userForm,'expenseForm':expenseForm,
            'doctor':models.Doctor.objects.get(user_id=request.user.id),}
    return render(request, 'hospital/doctor_add_expense.html',context=mydict)






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_expense_view(request):
    #those whose approval are needed
    expense=models.Expense.objects.all().filter(status=False)
    #messages.success(request,"Admin has approved Expense successfully.")
    return render(request,'hospital/admin_approve_expense.html',{'expense':expense})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_expense_view(request,pk):
    expense=models.Expense.objects.get(id=pk)
    expense.status=True
    expense.save()
    messages.success(request,"Expense approved successfully.")
    return redirect(reverse('admin-approve-expense'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_expense_view(request,pk):
    expense=models.Expense.objects.get(id=pk)
    user=models.User.objects.get(id=expense.user_id)
    messages.warning(request,"Expense rejected successfully.")
    #user.delete()
    expense.delete()
    return redirect('admin-approve-expense')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_expense_view(request,pk):
    expense=models.Expense.objects.get(id=pk)
    user=models.User.objects.get(id=expense.user_id)
    messages.warning(request,"Expense deleted successfully.")
    #user.delete()
    expense.delete()
    return redirect('admin-view-expense')



def delete_expense_view(request,pk):
    expense=models.Expense.objects.get(id=pk)
    user=models.User.objects.get(id=expense.user_id)
    messages.warning(request,"Expense deleted successfully.")
    #user.delete()
    expense.delete()
    return redirect('admin-view-expense')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_expense_view(request,pk):
    expense=models.Expense.objects.get(id=pk)
    user=models.User.objects.get(id=expense.user_id)
    userForm=forms.ExpenseUserForm(instance=user)
    expenseForm=forms.ExpenseForm(instance=expense)
    mydict={'userForm':userForm,'expenseForm':expenseForm}
    if request.method=='POST':
        userForm=forms.ExpenseUserForm(request.POST,instance=user)
        expenseForm=forms.ExpenseForm(request.POST,instance=expense)
        if expenseForm.is_valid():
            expense=expenseForm.save(commit=False)
            expense.save()
            messages.success(request,"Expense updated Successfully.")
            return redirect('admin-expense-view')
    return render(request,'hospital/admin_update_expense.html',context=mydict)




#Developed By : KENNEDY MAINIMO TATAH
