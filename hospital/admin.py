from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Income,Expense,AdminSigup,DoctorDischargeDetails
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


class DoctorDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(DoctorDischargeDetails, DoctorDischargeDetailsAdmin)


class IncomeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Income)

class ExpenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Expense)

admin.site.register(AdminSigup)