from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',home,name="home"),
    path("",main_login,name='main_login'),
    path("main_login/",main_login,name='main_login'),
    path("admin_login/",admin_login,name='admin_login'),
    path("admin_dash/",admin_dash,name='admin_dash'),
    path("add_doctor_page/",add_doctor_page,name='add_doctor_page'),
    path("admin_doctor/",admin_doctor,name='admin_doctor'),
    path("doctor_login/",doctor_login,name='doctor_login'),
    path("doctor_record/",doctor_record,name='doctor_record'),
    path("registration_form/",registration_form,name='registration_form'),
    path("user_login/",user_login,name='user_login'),
    path("add_doctor/",add_doctor,name='add_doctor'),
    path("approve_doctor_page/",approve_doctor_page,name='approve_doctor_page'),
    path("approve_doctor/<int:id>",approve_doctor,name='approve_doctor'),
    path("approve_doctor_view/",approve_doctor_view,name='approve_doctor_view'),
    path("delete_appdocrecord/<int:id>",delete_appdocrecord,name='delete_appdocrecord'),
    path("delete_docrecord/<int:doctor_id>",delete_docrecord,name='delete_docrecord'),
    path('update_docrecord/<int:doctor_id>',update_docrecord,name='update_docrecord'),
    path('admin_view_doctor/<int:doctor_id>',admin_view_doctor,name='admin_view_doctor'),
    # path('update_doc_image/<int:doctor_id>',update_doc_image,name='update_doc_image'),
    path('log_out/',log_out,name='log_out'),
]

#-------------------------------------------admin-patients
urlpatterns +=[
    path("admin_patient/",admin_patient,name='admin_patient'),
    path("patient_record/",patient_record,name='patient_record'),
    path('add_patient/',add_patient,name='add_patient'),
    path('add_patient_page/',add_patient_page,name='add_patient_page'),
    path('delete_patrecord/<int:patient_id>',delete_patrecord,name='delete_patrecord'),
    path('update_patrecord/<int:patient_id>',update_patrecord,name='update_patrecord'),
    path('update_patient/<int:patient_id>',update_patient,name=''),
    path('view_pat_invoice/<int:discharge_id>',view_pat_invoice,name='view_pat_invoice'),
    path('admin_view_patient/',admin_view_patient,name='admin_view_patient'),
]
#-------------------------------------admin-discharged patients
urlpatterns +=[
    path('discharge_patients/',discharge_patients,name='discharge_patients'),
    path('delete_dispatrecord/<int:patient_id>',delete_dispatrecord,name='delete_dispatrecord'),
]
#------------------------------------------admin-appointment
urlpatterns +=[
    path('appointment_record/',appointment_record,name='appointment_record'),
    path('add_appointment/',add_appointment,name='add_appointment'),
    path('admin_view_appointment/',admin_view_patient,name='admin_view_appointment'),
    path('delete_apprecord/<int:id>',delete_apprecord,name='delete_apprecord'),
    path('update_apprecord/<int:id>',update_apprecord,name='update_apprecord'),
    # path('view_app_invoice/<int:id>',view_app_invoice,name='view_app_invoice'),
]
#----------------------------------contact-us
urlpatterns +=[
    path('update_doc/<int:doctor_id>',update_doc,name='update_doc'),
    path('admin_contact/',admin_contact,name='admin_contact'),
    path('delete_contact/<int:id>',delete_contact,name='delete_contact'),
    path('admin_view_contact/',admin_view_contact,name='admin_view_contact'),
]


#---------------------------------------------------------------------------------------New urls------------------------------------------------
urlpatterns+=[
   path('contactus/',contactus,name="contactus"),
   path('contactussuccess/',contactussuccess,name="contactussuccess"),
   path('aboutus/',aboutus,name="aboutus"),
   path('doctorclick/',doctorclick,name="doctorclick"),
   path('doctorviewpatient/',doctorviewpatient,name="doctorviewpatient"),
#    path('doctorupdatepatient/<str:pk>',views.doctorupdatepatient,name="doctorupdatepatient"),
   path('doctorlogin/',doctorlogin,name="doctorlogin"),
   path('doctorsignup/',doctorsignup,name="doctorsignup"),
#    path('registrationsuccess',views.registrationsuccess,name="registrationsuccess"),
   path('doctorhome/',doctorhome,name="doctorhome"),
   path('doctordeletepatient/<str:pk>/',doctordeletepatient,name="doctordeletepatient"),
   path('doctorlogout/',doctorlogout,name='doctorlogout'),
   path('doctorprofile/',doctorprofile,name='doctorprofile'),
    path('doctorupdateprofile/',doctorupdateprofile,name='doctorupdateprofile'),
   path('doctor_feedback/',doctor_feedback,name='doctor_feedback'),
]


urlpatterns+=[
   path('patientclick/',patientclick,name="patientclick"),
   path('patientlogin/',patientlogin,name="patientlogin"),
   path('patientsignup/',patientsignup,name="patientsignup"),
   path('patienthome/',patienthome,name="patienthome"),
#    path('patientregistrationsuccess',views.pregsuccess,name="pregsuccess"),
   path('patient/<str:pk>',patient,name='patient'),
   path('patientlogout/',patientlogout,name='patientlogout'),
   path('patient_feedback/',patient_feedback,name='patient_feedback'),

]

urlpatterns+=[
   path('bookappointment',bookappointments,name="bookappointment"),
   path('viewappointments',viewappointments,name="viewappointments"),
   path('appointmentdelete/<str:pk>',deleteappointment,name="deleteappointment"),
   path('appointmentsuccess',appointmentsuccess,name="appointmentsuccess"),
   path('appointmentlimit',appointmentlimit,name="appointmentlimit"),
   path('get_doctors_by_department/',get_doctors_by_department, name='get_doctors_by_department'),
   # path('appointmentapprove',views.appointmentapprove,name="appointmentapprove"),
]

urlpatterns+=[
    path('reportform',reportform,name="reportform"),
    path('patientreportview',userreport,name="patientreportview"),
    path('report',report,name="report"),
]

urlpatterns+=[
    path('department/<int:id>/',department, name='departmentdoctors'),
]

#------------------------------------MEDIA URLS-------------------------------------------

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
