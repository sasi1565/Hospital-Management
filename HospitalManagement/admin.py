from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(sample)
admin.site.register(admins)
admin.site.register(patients)
admin.site.register(Doctorreg)
admin.site.register(approve_doctors)
# admin.site.register(Appointment)
admin.site.register(Departments)
admin.site.register(ReportHistory)
admin.site.register(Patientreg)
class ReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'report','id')
