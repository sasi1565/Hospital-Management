from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponseForbidden,JsonResponse
from .models import *
from .forms import *
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password,check_password



# Create your views here.
def admin_login_required(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not is_authenticated(request):
                messages.error(request,'Please login first to get Access')
                return redirect(login_url) if login_url else HttpResponseForbidden("Access denied")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def is_authenticated(request):
     user=request.session.get('admin_id')
     if(user):
          return True
     else:
        return False

def main_login(request):
    return render(request,'admin/main_login.html',{})

def admin_login(request):
    if request.method=="POST":
        admins_names=admins.objects.values_list('username',flat=True)
        admins_ids=admins.objects.values_list('admin_id',flat=True)
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username in admins_names  or username in admins_ids:
            print(username)
            if len(username)==3:
                admin_id1=admins.objects.get(pk=username)
            elif len(username)==6:
                admin_id1=admins.objects.filter(username=username).first()
            if admin_id1.password==password:
                doc_records=Doctorreg.objects.all().count()
                pat_records=patients.objects.all().count()
                app_records=Appointment.objects.all().count()
                request.session['admin_id']=username
                context={"doc_records":doc_records,
                        "pat_records":pat_records,
                        'admin_id':username,
                        'app_records':app_records
                    }
                return render(request,'admin/admin_dash.html',context)
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('admin_login')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('admin_login')
    return render(request,'admin/admin_login.html')


def log_out(request):
    request.session.clear()
    return redirect('main_login')

@admin_login_required(login_url='admin_login')
def admin_dash(request):
    admin_id=request.session.get('admin_id')
    if(admin_id is not None):
        doc_records=Doctorreg.objects.all().count()
        pat_records=patients.objects.all().count()
        app_records = Appointment.objects.all().count()
        context={"doc_records":doc_records,
                 "pat_records":pat_records,
                 "app_records":app_records,
                 'admin_id':admin_id}
        return render(request,'admin/admin_dash.html',context)
    else:
        loginmsg="Please Login First to get access"
        context = {
            'loginmsg':loginmsg,
            'admin_id':admin_id
        }
        return render(request,'admin/admin_login.html',context)
    
#-----------------------------------------------------doctors
@admin_login_required(login_url='admin_login')
def add_doctor_page(request):
    form = DoctorregForm()
    admin_id=request.session.get('admin_id')
    if(admin_id):
        current_date=timezone.now().date().strftime("%Y-%m-%d")
        context = {
            'current_date':current_date,
            'admin_id':admin_id,
            'form':form
        }
        return render(request,'admin/add_doctor.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/add_doctor.html',context)
    

@admin_login_required(login_url='admin_login')
def add_doctor(request):
    if request.method=="POST":
        dd=Doctorreg()
        last_instance=Doctorreg.objects.all().order_by("-doctor_id").first()
        if last_instance is None:
            u_id=1000
        else:
            doc_id=last_instance.doctor_id
            u_id=doc_id+1
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        password=request.POST.get("password")
        con_password=request.POST.get("con-password")
        age = request.POST.get("age")
        username=request.POST.get("username")
        form=DoctorregForm(request.POST)
        if form.is_valid():  
                department=form.cleaned_data['department']
        date=request.POST.get("date")
        mobile=request.POST.get("mobileno")
        address=request.POST.get("address")
        experience=request.POST.get('experience')
        image = request.FILES['image']
        if(password!=con_password):
            messages.error(request,'Please check the Password')
            return redirect('add_doctor_page')
        try:
            validate_password(password)
        except:
            messages.error(request,'Password is not strong, Try a different password including atleast 8 charachters and numbers')
            return redirect('add_doctor_page')
        
        dd.doctor_id=u_id
        dd.email=email
        dd.firstname=firstname
        dd.lastname=lastname
        dd.username=username
        dd.password=make_password(password)
        dd.age=age
        dd.gender=request.POST.get('gender')
        dd.qualification=request.POST.get('qualification')
        dd.date=date
        dd.mobile=mobile
        dd.address=address
        dd.department=department
        dd.experience=experience
        dd.image=image
        dd.save()
        messages.success(request,'Registered Successfully')
        return redirect('admin_doctor')
    return render(request,'admin/add_doctor.html')


@admin_login_required(login_url='admin_login')
def approve_doctor_page(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        data=approve_doctors.objects.all()
        context = {
            'data':data
        }
        return render(request,'admin/approve_doctor.html',context)
    else:
        return redirect('admin_login')
    

@admin_login_required(login_url='admin_login')    
def approve_doctor(request,id):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        record=approve_doctors.objects.get(pk=id)
        dd=Doctorreg()
        last_instance=Doctorreg.objects.all().order_by("-doctor_id").first()
        if last_instance is None:
            u_id=1000
        else:
            doc_id=last_instance.doctor_id
            u_id=doc_id+1
        email=record.email
        firstname=record.firstname
        lastname=record.lastname
        password=record.password
        department=record.department
        mobile=record.mobile
        address=record.address
        experience=record.experience
        image = record.image
            
        dd.doctor_id=u_id
        dd.email=email
        dd.firstname=firstname
        dd.username=record.username
        dd.age=record.age
        dd.qualification=record.qualification
        dd.lastname=lastname
        dd.password=password
        dd.gender=record.gender
        dd.date=timezone.now().date().strftime("%Y-%m-%d")
        dd.mobile=mobile
        dd.address=address
        dd.department=department
        dd.experience=experience
        dd.image=image
        dd.save()
        subject = 'You have been approved'
        message = f'Your Application Has been approved by the admin.\nYou can now login to your account using the \nUsername: {record.username} \nAnd the password you have entered while registering.\nThank You'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        sent = send_mail(subject, message, from_email, recipient_list)
        record.delete()
        if sent:
            messages.success(request, 'Approval email Sent')
            return redirect('approve_doctor_page')
        else:
            messages.error(request, 'An error occurred while sending the Approval email.')
            return redirect('approve_doctor_page')
    else:
        return redirect('admin_login')
    
@admin_login_required(login_url='admin_login')
def delete_appdocrecord(request,id):
    record=approve_doctors.objects.get(pk=id)
    record.delete()
    return redirect('approve_doctor_page')
    
@admin_login_required(login_url='admin_login')
def approve_doctor_view(request):
    return HttpResponseRedirect(reverse('approve_doctor_view'))

@admin_login_required(login_url='admin_login')
def delete_docrecord(request,doctor_id):
    record=Doctorreg.objects.get(pk=doctor_id)
    record.delete()
    return redirect('doctor_record')


@admin_login_required(login_url='admin_login')
def update_docrecord(request,doctor_id):
    record=Doctorreg.objects.get(pk=doctor_id)
    initial_data= {'department':record.department}
    form=DoctorregForm(initial=initial_data)
    context = {
        "record":record,
        'form':form
    }
    return render(request,"admin/update_doctor.html",context)

@admin_login_required(login_url='admin_login')
def update_doc(request,doctor_id):
    if request.method=="POST":
        record=Doctorreg.objects.get(pk=doctor_id)
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        password=request.POST.get("password")
        date=request.POST.get("date")
        department=request.POST.get("department")
        mobile=request.POST.get("mobileno")
        username=request.POST.get("username")
        experience=request.POST.get('experience')
        # image=request.FILES['image']
        address=request.POST.get("address")
        # print(image)
        # if image:
        #     update_doc_image(doctor_id,image)
        form=DoctorregForm(request.POST)
        if form.is_valid():  
            department=form.cleaned_data['department']
        try:
            validate_password(password)
        except:
            messages.info(request,'Password is not strong, Try a different password including atleast 8 charachters and numbers')
            context = {
                'record':record,
            }
            return render(request,"admin/update_doctor.html",context)
        
        
        record.email=email
        record.firstname=firstname
        record.lastname=lastname
        hashedpassword=make_password(password)
        if(record.password==password):
            record.password=password
        else:
            record.password=hashedpassword
        record.date=date
        record.mobile=mobile
        record.username=username   
        record.address=address
        record.department=department
        record.experience=experience
        record.save()
        messages.success(request,'Updated Successfully')
        return redirect("doctor_record")
    return redirect("doctor_record")

# def update_doc_image(doctor_id,image):
#         record=doctors.objects.get(pk=doctor_id)
#         record.image=image

@admin_login_required(login_url='admin_login')
def admin_view_doctor(request,doctor_id):
    return HttpResponseRedirect(reverse('admin_view_doctor'))


@admin_login_required(login_url='admin_login')
def admin_doctor(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        data=Doctorreg.objects.all().order_by("-doctor_id")[:4]
        context = {
            'admin_id':admin_id,
            "data":data
        }
        return render(request,'admin/admin_doctor.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/admin_doctor.html', context )

@admin_login_required(login_url='admin_login')
def registration_form(request):
    return render(request,'Registration-form.html')

# def doctor_record(request):
#     if request.method=="POST":
#         doc_id1=request.POST.get('doc_id')
#         data=doctors.objects.filter(doctor_id=doc_id1)
#         print(data)
#         if data.count()==0:
#             msg="No Doctor Found with the Doctor ID"
#             return render(request,"doctor_record.html",{"msg":msg})
#         else:
#             return render(request,"doctor_record.html",{"data":data})
#     data=doctors.objects.all()
#     return render(request,'doctor_record.html',{"data":data})


@admin_login_required(login_url='admin_login')
def doctor_record(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        if request.method=="POST":
            doc_id1=request.POST.get('doc_id')
            try:
                data=Doctorreg.objects.filter(doctor_id=doc_id1)
            except:
                messages.error(request,'Please enter a valid Doctor ID')
                return redirect('doctor_record')
            print(data)
            if data.count()==0:
                msg="No Doctor Found with the Doctor ID"
                return render(request,"admin/doctor_record.html",{"msg":msg})
            else:
                return render(request,"admin/doctor_record.html",{"data":data})
        data=Doctorreg.objects.all()
        return render(request,'admin/doctor_record.html',{"data":data})
    else:
        return redirect('admin_login')


def user_login(request):
    return render(request,'admin/user_login.html')

#------------------------------------------Feedback

@admin_login_required(login_url='admin_login')
def admin_contact(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        data=feedback_data.objects.all()
        context = {
            'data':data,
            'admin_id':admin_id
        }
        return render(request,'admin/admin_feedback.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/admin_feedback.html',context)

@admin_login_required(login_url='admin_login')    
def admin_view_contact(request):
    return HttpResponseRedirect(reverse('admin_view_contact'))
   

@admin_login_required(login_url='admin_login')
def delete_contact(request,id):
    record=feedback_data.objects.get(pk=id)
    record.delete()
    return redirect('admin_contact')

@admin_login_required(login_url='admin_login')
def send_res(request,id):
    return HttpResponseRedirect(reverse('admin_view_contact'))
#--------------------------------Doctor Login

@admin_login_required(login_url='admin_login')
def doctor_login(request):
    if request.method=='POST':
        doc_id=request.POST.get('doc_id')
        password=request.POST.get('doc_pass')
        data=Doctorreg.objects.get(pk=doc_id)
        if data.password==password:
            return redirect('admin_dash')
        else:
            return redirect('doctor_login')
    return render(request,'admin/doctor_login.html')

#---------------------------------------admin-patient
@admin_login_required(login_url='admin_login')
def admin_patient(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        data=patients.objects.all().order_by("-patient_id")[:4]
        context = {
            'admin_id':admin_id,
            'data':data
        }
        return render(request,'admin/admin_patient.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/admin_patient.html',context)
    

@admin_login_required(login_url='admin_login')    
def patient_record(request):
    if request.method=="POST":
        pat_id=request.POST.get('pat_id')
        try:
            data=patients.objects.filter(patient_id=pat_id)
        except:
            messages.error(request,'Please enter a valid Patient ID')
            return redirect('patient_record')
        print(data.count())
        count=1
        if data.count()==0:
            msg="No Patients Found with the Patient ID"
            return render(request,"admin/patient_record.html",{"msg":msg})
        else:
            context = {
                "data":data,
                'count':count
            }
            return render(request,"admin/patient_record.html",context)
    data=patients.objects.all()
    context = {
        'data':data
    }
    return render(request,'admin/patient_record.html',context)

@admin_login_required(login_url='admin_login') 
def add_patient_page(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        form = PatientForm()
        current_date=timezone.now().date().strftime("%Y-%m-%d")
        departments=Departments.objects.all()
        context = {
            'admin_id':admin_id,
            'current_date':current_date,
            'form':form,
            'departments':departments   
        }
        return render(request,'admin/add_patient.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/add_patient.html',context)
    

@admin_login_required(login_url='admin_login')
def add_patient(request):
    if request.method=="POST":
        pat=patients()
        last_instance=patients.objects.all().order_by("-patient_id").first()
        if last_instance is None:
            u_id=5000
        else:
            pat_id=last_instance.patient_id
            u_id=pat_id+1
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        app_date=request.POST.get("date")
        age=request.POST.get("age")
        symptoms=request.POST.get("symptoms")
        description=request.POST.get("description")
        mobileno=request.POST.get("mobileno")
        address=request.POST.get("address")
        image=request.FILES['image']

        pat.patient_id=u_id
        pat.email=email
        pat.firstname=firstname
        pat.lastname=lastname
        pat.age=age
        pat.department_id=request.POST.get("department")
        pat.doctor_id=request.POST.get("doctor")
        pat.app_date=app_date
        pat.mobileno=mobileno
        pat.address=address
        pat.symptoms=symptoms
        pat.description=description
        pat.image=image
        pat.save()
        messages.success(request,'Registered Successfully')
        return redirect('admin_patient')
    
@admin_login_required(login_url='admin_login')
def delete_patrecord(request,patient_id):
    record=patients.objects.get(pk=patient_id)
    dis=discharged_patients()
    last_instance=discharged_patients.objects.all().order_by("-discharge_id").first()
    if last_instance is None:
        u_id=1000
    else:
        doc_id=last_instance.discharge_id
        u_id=doc_id+1
    dis.discharge_id=u_id
    dis.email=record.email
    dis.firstname=record.firstname
    dis.lastname=record.lastname
    dis.age=record.age
    dis.app_date=record.app_date
    dis.dis_date=timezone.now().date().strftime("%Y-%m-%d")
    dis.mobileno=record.mobileno
    dis.symptoms=record.symptoms
    dis.description=record.description
    dis.app_or_pat=1
    dis.save()
    record.delete()
    return  redirect('patient_record')

@admin_login_required(login_url='admin_login')
def admin_view_patient(request):
    return HttpResponseRedirect(reverse('admin_view_patient'))

@admin_login_required(login_url='admin_login')
def discharge_patients(request):
    if request.method=="POST":
        try:
            pat_id=request.POST.get('pat_id')
            data=discharged_patients.objects.filter(discharge_id=pat_id)
        except:
            messages.error(request,'Please enter a valid Discharge ID')
            return redirect('discharge_patients')
        if data.count()==0:
            msg="No Patients Found with the Patient ID"
            return render(request,"admin/discharged_patients.html",{"msg":msg})
        else:
            context= {
                "data":data
            }
            return render(request,"admin/discharged_patients.html",context)
    data=discharged_patients.objects.all()
    context= {
                "data":data
    }
    return render(request,'admin/discharged_patients.html',context)


@admin_login_required(login_url='admin_login')
def delete_dispatrecord(request,patient_id):
    record=discharged_patients.objects.get(pk=patient_id)
    record.delete()
    return  redirect('discharge_patients')

@admin_login_required(login_url='admin_login')
def update_patrecord(request,patient_id):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        record=patients.objects.get(pk=patient_id)
        dept=Departments.objects.all()
        initial_data= {'department':record.department}
        form=PatientForm(initial=initial_data)
        context = {
            'record':record,
            'admin_id':admin_id,
            'dept':dept,
            'form':form
        }
        return render(request,'admin/update_patient.html',context)
    else:
       loginmsg="Please Login First to get access"
       context = {
           'loginmsg':loginmsg,
           'admin_id':admin_id
       }
       return render(request,'admin/admin_patient.html',context)


@admin_login_required(login_url='admin_login')
def update_patient(request,patient_id):
    if request.method=="POST":
        pat=patients.objects.get(pk=patient_id)
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        app_date=request.POST.get("date")
        age=request.POST.get("age")
        symptoms=request.POST.get("symptoms")
        description=request.POST.get("description")
        mobileno=request.POST.get("mobileno")
        address=request.POST.get("address")
        form=PatientForm(request.POST)
        if form.is_valid():  
            department=form.cleaned_data['department']

        pat.email=email
        pat.firstname=firstname
        pat.lastname=lastname
        pat.age=age
        pat.department=department
        pat.gender=request.POST.get("gender")
        pat.app_date=app_date
        pat.mobileno=mobileno
        pat.address=address
        pat.symptoms=symptoms
        pat.description=description
        pat.save()
        messages.success(request,'Updated Successfully')
        return redirect("patient_record")

#----------------------------Patient Invoice

hospital_fee=300
appointment_fee=300 

# @admin_login_required(login_url='admin_login')
# def view_pat_invoice(request,patient_id):
#     admin_id=request.session.get('admin_id')
#     if(admin_id):
#         global hospital_fee
#         patient=patients.objects.get(pk=patient_id)
#         bill_date=timezone.now().date().strftime("%Y-%m-%d")#%d-%m-%Y
#         curr_date=timezone.now().date().strftime("%Y-%m-%d")
#         date_format = "%Y-%m-%d"
#         curr_date=datetime.strptime(curr_date, date_format)
#         date_obj = datetime.strptime(patient.app_date, date_format)
#         diff=curr_date-date_obj
#         day=diff.days
#         total_hos_fee=hospital_fee*day
#         doctor_fee=500
#         total_bill=total_hos_fee+doctor_fee
#         context = {
#             "pat":patient,
#             "bill_date":bill_date,
#             "day":day,
#             "total_hos_fee":total_hos_fee,
#             "doctor_fee":doctor_fee,
#             "total_bill":total_bill
#         }
#         return render(request,'admin/patient_invoice.html',context)
#     else:
#         return redirect('admin_login')
    

@admin_login_required(login_url='admin_login')
def view_pat_invoice(request,discharge_id):
    pat=discharged_patients.objects.get(pk=discharge_id)
    if(pat.app_or_pat==1):
        global hospital_fee
        bill_date=timezone.now().date().strftime("%Y-%m-%d")#%d-%m-%Y
        curr_date=timezone.now().date().strftime("%Y-%m-%d")
        date_format = "%Y-%m-%d"
        curr_date=datetime.strptime(curr_date, date_format)
        date_obj = datetime.strptime(pat.app_date, date_format)
        diff=curr_date-date_obj
        day=diff.days
        total_hos_fee=hospital_fee*day
        doctor_fee=500
        total_bill=total_hos_fee+doctor_fee
        bill_date=timezone.now().date().strftime("%d-%m-%Y")
        context = {
            "pat":pat,
            "bill_date":bill_date,
            "day":day,
            "total_hos_fee":total_hos_fee,
            "doctor_fee":doctor_fee,
            "total_bill":total_bill
        }
        return render(request,'admin/patient_invoice.html',context)
    else:
        global appointment_fee
        app=discharged_patients.objects.get(pk=discharge_id)
        bill_date=timezone.now().date().strftime("%d-%m-%Y")#%d-%m-%Y
        appointment_fee=500
        context = {
            "app":app,
            "bill_date":bill_date,
            "appointment_fee":appointment_fee,
        }
        return render(request,'admin/appointment_invoice.html',context)
# def add_admin(request):
#     if request.method=="POST":
#         admin=admins()
#         admin.admin_id=102
#         admin.username='admin2'
#         admin.password='5678'
#         admin.save()
#         return redirect('/admin_login/')
#     return render(request,'add_admin.html')

# doc_ids=doctors.objects.values_list('doctor_id',flat=True)
        # if doc_id in doc_ids:
        #     data=doctors.objects.filter(doctor_id=doc_id).values()
        #     return render(request,"doctor_record.html",{"data":data})
        # else:
        #     messages.error(request,'Invalid DoctorID')
        #     return redirect("/doctor_record/")

#--------------appointment

@admin_login_required(login_url='admin_login')
def appointment_record(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        data = Appointment.objects.all()
        if request.method=='POST':
            id=request.POST.get('id')
            try:
                data=Appointment.objects.filter(id=id)
            except:
                messages.error(request,'Please enter a valid Patient ID')
                return redirect('appointment_record')
            print(data.count())
            count=1
            if data.count()==0:
                msg="No Appointments Found with the Appointment ID"
                return render(request,"admin/appointment_record.html",{"msg":msg})
            else:
                context = {
                    "data":data,
                    'count':count
                }
                return render(request,"admin/appointment_record.html",context)
        context = {
            'admin_id':admin_id,
            'data':data
        }
        return render(request,'admin/appointment_record.html',context)
    else:
        messages.error(request,'Please Login First')
        return redirect('admin_login')
    
@admin_login_required(login_url='admin_login')   
def add_appointment(request):
    admin_id=request.session.get('admin_id')
    if(admin_id):
        if request.method=="POST":
            app=Appointment()
            email=request.POST.get("email")
            firstname=request.POST.get("firstname")
            lastname=request.POST.get("lastname")
            app_date=request.POST.get("date")
            age=request.POST.get("age")
            symptoms=request.POST.get("symptoms")
            description=request.POST.get("description")
            mobileno=request.POST.get("phone")
            form=AppointmentForm(request.POST)
            if form.is_valid():  
                department=form.cleaned_data['department']
            app.email=email
            app.firstname=firstname
            app.lastname=lastname
            app.department=department
            app.gender=request.POST.get('gender')
            app.doctor_id=request.POST.get("doctor") 
            app.age=age
            app.date=app_date
            app.phone=mobileno
            app.symptoms=symptoms
            app.description=description
            app.save()
            subject = 'Appointment Booked'
            message = 'Your appointment for the date '+app_date+' to HOSPITAL MANAGEMENT SYSTEM is successful.Thank you!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            sent = send_mail(subject, message, from_email, recipient_list)
            if sent:
                messages.success(request, 'Appointment created Successfully! Confirmation email sent.')
                return redirect('appointment_record')
            else:
                messages.error(request, 'An error occurred while sending the confirmation email.')
                return redirect('appointment_record')
        departments=Departments.objects.all()
        current_date=timezone.now().date().strftime("%Y-%m-%d")
        form=AppointmentForm()
        context = {
            'admin_id':admin_id,
            'departments':departments,
            'current_date':current_date,
            'form':form
        }
        return render(request,'admin/add_appointment.html',context)
    else:
        messages.error(request,'Please Login First')
        return redirect('admin_login')
    
@admin_login_required(login_url='admin_login')    
def admin_view_appoinment(request):
    return HttpResponseRedirect(reverse('admin_view_appointment'))

@admin_login_required(login_url='admin_login')
def delete_apprecord(request,id):
    record=Appointment.objects.get(pk=id)
    dis=discharged_patients()
    last_instance=discharged_patients.objects.all().order_by("-discharge_id").first()
    if last_instance is None:
        u_id=10000
    else:
        doc_id=last_instance.discharge_id
        u_id=doc_id+1
    dis.discharge_id=u_id
    dis.email=record.email
    dis.firstname=record.firstname
    dis.lastname=record.lastname
    dis.age=record.age
    dis.app_date=record.date
    dis.dis_date=timezone.now().date().strftime("%Y-%m-%d")
    dis.mobileno=record.phone
    dis.symptoms=record.symptoms
    dis.description=record.description
    dis.app_or_pat=0
    dis.save()
    record.delete()
    return redirect('appointment_record')

@admin_login_required(login_url='admin_login')
def update_apprecord(request,id):
    admin_id=request.session.get('admin_id')
    record=Appointment.objects.get(pk=id)
    initial_data= {'department':record.department}
    form=AppointmentForm(initial=initial_data)
    # date_format = "%Y-%m-%d"
    # date=datetime.strftime(record.date, date_format)
    if request.method=="POST":
            email=request.POST.get("email")
            firstname=request.POST.get("firstname")
            lastname=request.POST.get("lastname")
            age=request.POST.get("age")
            symptoms=request.POST.get("symptoms")
            description=request.POST.get("description")
            mobileno=request.POST.get("mobileno")
            form=AppointmentForm(request.POST)
            if form.is_valid():  
                department=form.cleaned_data['department']
            record.email=email
            record.firstname=firstname
            record.lastname=lastname
            record.department=department
            record.age=age
            record.phone=mobileno
            # record.doctor=request.POST.get("doctor_id")
            record.symptoms=symptoms
            record.description=description
            record.save()
            messages.success(request,'Appointment Updated Successfully')
            return redirect('appointment_record')
    context = {
        'record':record,
        'admin_id':admin_id,
        'date':record.date,
        'form':form
    }
    return render(request,'admin/update_appointment.html',context)

#---------------------appointment invoice

# @admin_login_required(login_url='admin_login')
# def view_app_invoice(request,id):
#     admin_id=request.session.get('admin_id')
#     if(admin_id):
#         global appointment_fee
#         app=Appointment.objects.get(pk=id)
#         bill_date=timezone.now().date().strftime("%d-%m-%Y")#%d-%m-%Y
#         appointment_fee=500
#         context = {
#             "app":app,
#             "bill_date":bill_date,
#             "appointment_fee":appointment_fee,
#         }
#         return render(request,'admin/appointment_invoice.html',context)
#     else:
#         return redirect('admin_login')
    
#----------------------------------------------------------------new-part---------------------------------------------

def doctor_login_required(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not is_doctor_authenticated(request):
                messages.error(request,'Please login first to get Access')
                return redirect(login_url) if login_url else HttpResponseForbidden("Access denied")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def is_doctor_authenticated(request):
     user=request.session.get('username')
     if(user):
          return True
     else:
        return False

# def home(request):
#     # q= request.GET.get('q','') if request.GET.get('q')!=None  else ''
#     # doctor=Doctorreg.objects.filter(Q(department__department__icontains=q)|
#     #                                 Q(firstname__icontains=q)|
#     #                                 Q(username__icontains=q))
#     # # doctor_count=doctor.count()
#     # has_firstname = bool(q) and 'firstname' in q.lower()
#     # topic=Depts.objects.all()
#     # context={'topics':topic,'doctors':doctor,'has_firstname': has_firstname}
#     doctor=Doctorreg.objects.all()
#     return render(request,'home.html',{'doctor':doctor}) 

def contactus(request):
    form=ContactusForm()
    if request.method == 'POST':
        form=ContactusForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name=form.cleaned_data['Name']
            message = form.cleaned_data['Message']
            subject="contactus-mail"
            from_email = email
            recipient_list =  [settings.EMAIL_HOST_USER]
            try:
                send_mail(subject, message, from_email,recipient_list )
            except:
                messages.error(request,'Sorry an error occurd while sending your message')
                return redirect('contactus')
            return redirect('contactussuccess')
        else:
            messages.error(request,'please try again!')
    return render(request,'contactus.html',{'form':form})

def contactussuccess(request):
    return render(request,'contactussuccess.html')

def aboutus(request):
    return render(request,'aboutus.html')

@doctor_login_required(login_url='doctorlogin')
def doctorviewpatient(request):
    patient=Appointment.objects.all()
    context={'patients':patient}
    return render(request,'doctor/doctor_viewpatient.html',context)
    
# @login_required(login_url='doctorlogin')
# def doctorupdatepatient(request,pk):
#     patient=Appointment.objects.get(pk=pk)
#     form= Appointments(instance=patient)

#     if request.method=='POST':
#         form=Appointments(request.POST,instance=patient)
#         if form.is_valid:
#             form.save()
#             return redirect('updationsuccess')
#     context={'form':form}
#     return render(request,'patient_signup.html',context)
    
@doctor_login_required(login_url='doctorlogin')
def doctordeletepatient(request,pk):
    record = Appointment.objects.get(pk=pk)
    if request.method=='POST':
        dis=discharged_patients()
        last_instance=discharged_patients.objects.all().order_by("-discharge_id").first()
        if last_instance is None:
            u_id=10000
        else:
            doc_id=last_instance.discharge_id
            u_id=doc_id+1
        dis.discharge_id=u_id
        dis.email=record.email
        dis.firstname=record.firstname
        dis.lastname=record.lastname
        dis.age=record.age
        dis.app_date=record.date
        dis.dis_date=timezone.now().date().strftime("%Y-%m-%d")
        dis.mobileno=record.phone
        dis.symptoms=record.symptoms
        dis.description=record.description
        dis.app_or_pat=0
        dis.save()
        record.delete()
        return redirect('doctorhome')
    return render(request,'doctor/doctor_deleteconfirm.html',{'obj':record})


def doctorclick(request):
    return render(request,'doctor/doctorclick.html')

def doctorsignup(request):
    if request.method == 'POST':
        doctorForm = DoctorForm1(request.POST, request.FILES)
        date=request.POST.get('date')
        gender=request.POST.get('gender')
        cpassword=request.POST.get('cpassword')
        password=request.POST.get('password')
        image=request.FILES['image']
        mobile=request.POST.get('mobile')
        if doctorForm.is_valid():
            username=doctorForm.cleaned_data['username']
            if(Doctorreg.objects.filter(username=username).exists()):
                messages.error(request,"Username already exists,Try with different username")
                return redirect('doctorsignup')
            try:
                validate_password(password)
            except:
                messages.error(request,'Password is not strong, Try a different password including atleast 8 charachters and numbers')
                return redirect('doctorsignup')
            if(cpassword==password):
                data = approve_doctors(
                    firstname=doctorForm.cleaned_data['firstname'],
                    lastname=doctorForm.cleaned_data['lastname'],
                    email=doctorForm.cleaned_data['email'],
                    experience=request.POST.get('experience'),
                    username=doctorForm.cleaned_data['username'],
                    age=doctorForm.cleaned_data['age'],
                    address=doctorForm.cleaned_data['address'],
                    gender=gender,
                    qualification=doctorForm.cleaned_data['qualification'],
                    mobile=mobile,
                    date=date,
                    department=doctorForm.cleaned_data['department'],
                    password=make_password(password),
                    image=image
                )
                data.save()
                messages.success(request,"Sucessfully Applied for Doctor,Wait for the Approval")
                # my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
                # my_doctor_group.user_set.add(user)
                context = {
                    'firstname':doctorForm.cleaned_data['firstname']
                }
                return render(request,'doctor/doctor_wait_for_approval.html',context)
                # user = userForm.save()
                # user.set_password(user.password)
                # user.save()
                # doctor = doctorForm.save(commit=False)
                # doctor.user = user
                # doctor.save()
            else:
                messages.error(request,"Please Check the Password")
                return redirect('doctorsignup')
            
        else:
            messages.error(request,"form is not validated!,Username Already exists Try with a different username")
            return redirect('doctorsignup')
    else:
        doctorForm = DoctorForm1()
        to_date = timezone.now().date().strftime("%Y-%m-%d")
        mydict = { 'doctorForm': doctorForm,
                'date': to_date
                }
        return render(request, 'doctor/doctor_signup.html', {'form': mydict})

@doctor_login_required(login_url='doctorlogin')
def doctor_feedback(request):
    if request.method=="POST":
        con=feedback_data()
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        con.name=name
        con.email=email
        con.message=message
        con.save()
        messages.success(request,'Thanks for your Feedback')
        return redirect('doctor_feedback')
    return render(request,'doctor/doctor_feedback.html')
# def doctorlogin(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         try:
#             user=User.objects.get(username=username)
#             doctor=doctors.objects.get(username=username)
#         except User.DoesNotExist:
#             messages.error(request,'No user with this username.')
#             return render(request, 'doctor_login.html')
#         except doctors.DoesNotExist:
#             messages.error(request, 'User is not a doctor.')
#             return render(request, 'doctor_login.html')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('doctorhome')
#         else:
#             messages.error(request,'enter valid password')
#     return render(request,'doctor_login.html')

def doctorlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            doctor=Doctorreg.objects.get(username=username)
        except Doctorreg.DoesNotExist:
            messages.error(request, 'Invalid username or Password')
            return render(request, 'doctor/doctor_login.html')
        if check_password(password, doctor.password):
            image=doctor.image.url
            request.session['username']=doctor.username
            request.session['image']=image
            return redirect('doctorhome')
        else:
            messages.error(request,'enter valid password')
    return render(request,'doctor/doctor_login.html')



@doctor_login_required(login_url='doctorlogin')   
def doctorhome(request):
    id=request.session.get('username')
    try:
        doctor=Doctorreg.objects.get(username=id)
    except Doctorreg.DoesNotExist:
        messages.error(request, 'No user found with this Doctor Id.')
        return render(request, 'doctor/doctor_login.html')
    department = doctor.department
    doctor_id=doctor.doctor_id
    print(department)
    appointments = Appointment.objects.filter(Q(department=department) & Q(doctor_id=doctor_id) )
    total = appointments.count()
    doctor_id=doctor.doctor_id
    context={'doctor_id':doctor_id,'appointment':appointments,'total':total,'doctor':doctor}
    return render(request,'doctor/doctor_dashboard.html',context)

@doctor_login_required(login_url='doctorlogin')
def doctorprofile(request):
    id=request.session.get('username')
    try:
        doctor=Doctorreg.objects.get(username=id)
    except Doctorreg.DoesNotExist:
        messages.error(request, 'No user found with this Doctor Id.')
        return render(request, 'doctor/doctor_login.html')
    context={'doctor':doctor}
    return render(request,'doctor/doctor_profile.html',context)

@doctor_login_required(login_url='doctorlogin')
def doctorupdateprofile(request):
    id=request.session.get('username')
    if request.method=='POST':
        doctor=Doctorreg.objects.get(username=id)
        doctor.firstname=request.POST.get('firstname')
        doctor.lastname=request.POST.get('lastname')
        doctor.email=request.POST.get('email')
        doctor.age=request.POST.get('age')
        doctor.qualification=request.POST.get('qualification')
        doctor.address=request.POST.get('address')
        doctor.mobile=request.POST.get('mobile')
        doctor.experience=request.POST.get('experience')
        doctor.save()
        return redirect('doctorprofile')
    try:
        doctor=Doctorreg.objects.get(username=id)
    except Doctorreg.DoesNotExist:
        messages.error(request, 'No user found with this Doctor Id.')
        return render(request, 'doctor/doctor_login.html')
    context={'doctor':doctor}
    return render(request,'doctor/update_profile.html',context)

# @doctor_login_required(login_url='doctorlogin')
# def doctor_feedback()


@doctor_login_required(login_url='doctorlogin')
def doctorlogout(request):
    request.session.clear()
    return redirect('main_login')
#----------------------------------------------------------------------------------:
def patient_login_required(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not is_patient_authenticated(request):
                messages.error(request,'Please login first to get Access')
                return redirect(login_url) if login_url else HttpResponseForbidden("Access denied")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def is_patient_authenticated(request):
     user=request.session.get('patient_username')
     if(user):
          return True
     else:
        return False


def patientclick(request):
    return render(request,'patient/patientclick.html')

def patient_feedback(request):
    if request.method=="POST":
        con=feedback_data()
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        con.name=name
        con.email=email
        con.message=message
        con.save()
        messages.success(request,'Thanks for you Feedback')
        return redirect('patient_feedback')
    return render(request,'patient/patient_feedback.html')

@patient_login_required(login_url='patientlogin')   
def patienthome(request):
    username=request.session['patient_username']
    patient=Patientreg.objects.get(username=username)
    departments=Departments.objects.all()
    return render(request,'patient/patient_home1.html',{'department':departments})

@patient_login_required(login_url='patientlogin') 
def patientlogout(request):
    request.session.clear()
    return redirect('main_login')

def patientlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            patient=Patientreg.objects.get(username=username)
        except Patientreg.DoesNotExist:
            messages.error(request, 'User is not a patient.')
            return render(request, 'patient/patient_login.html')
        # user = authenticate(request, username=user.username, password=password)
        # if user is not None:
        #     login(request,user)
        #     return redirect('patienthome')
        # else:
        #     messages.error(request,'enter valid password')
        if check_password(password, patient.password):
            username=patient.username
            request.session['patient_username']=username
            return redirect('patienthome')
        else:
            messages.error(request,'enter valid password')
    return render(request,'patient/patient_login.html')


def patient(request,pk):
    patients=Appointment.objects.get(id=pk)
    appointments=Appointment.objects.filter(id=pk)
    context={'patient':patients,'appointments':appointments}
    return render(request,'patient/patient.html',context)

def pregsuccess(request):
    return render(request,'patient/patient_registrationsuccess.html')

def patientsignup(request):
    if request.method=='POST':
        form=Patientregs(request.POST)
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if form.is_valid():
            if(cpassword==password):
                try:
                    validate_password(password)
                except:
                    messages.error(request,'Password is not strong, Try a different password including atleast 8 charachters and numbers')
                    return redirect('patientsignup')
                data = Patientreg(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(password),
                )
                data.save()
                messages.success(request,"Sucessfully Registered,Login to continue")
                return redirect('patientlogin')
            else:
                messages.error(request,"Please Check the Password")
                return redirect('patientsignup')
        else:
            messages.error(request,'An error has occured during registration')
    else:
        form=Patientregs()
    context={'form':form}
    return render(request,'patient/patient_signup.html',context)

@patient_login_required(login_url='patientlogin') 
def userreport(request):
    id=request.session.get('patient_username')
    # try:
    #     doctor=Patientreg.objects.get(username=id)
    # except Doctorreg.DoesNotExist:
    #     messages.error(request, 'No user found with this Doctor Id.')
    #     return render(request, 'doctor/doctor_login.html')
    username = request.session.get('patient_username')
    patient_instance = get_object_or_404(Patientreg, username=username)
    data = ReportHistory.objects.filter(patient=patient_instance)
    context={
        'instance':data,
        # 'doctor':doctor
        }
    
    return render(request, 'patient/patient_reportview.html',context )

#------------appointments------------------------------------------
@patient_login_required(login_url='patientlogin')
def bookappointments(request):
    appointments=Appointment.objects.all()
    department=Departments.objects.all()
    date=timezone.now().date().strftime("%Y-%m-%d")
    count=appointments.count()
    doc_id=request.POST.get('doctor')
    print(count)
    if(count>100):
        return redirect('appointment/appointmentlimit')
    else:
        if request.method=='POST':
            form=Appointments(request.POST)
            date=request.POST.get('date')
            phone=request.POST.get('phone')
            if form.is_valid():
                data = Appointment(
                    firstname=form.cleaned_data['firstname'],
                    lastname=form.cleaned_data['lastname'],
                    email=form.cleaned_data['email'],
                    age=form.cleaned_data['age'],
                    phone=phone,
                    doctor_id=request.POST.get('doctor'),
                    date=date,
                    symptoms=form.cleaned_data['symptoms'],
                    department=form.cleaned_data['department'],
                    description=form.cleaned_data['description']
                    )
                data.save()
                doctor=Doctorreg.objects.get(doctor_id=doc_id)

                patient_mail=form.cleaned_data['email']
                subject = 'Appointment Booked'
                message = f'Your appointment into HOSPITAL MANAGEMENT SYSTEM with Dr.{doctor.firstname} {doctor.lastname} is successful.Thank you!'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [patient_mail]
                sent = send_mail(subject, message, from_email, recipient_list)
                if sent:
                    messages.success(request, 'Registration successful! Confirmation email sent.')
                    return redirect('bookappointment')
                else:
                    messages.error(request, 'An error occurred while sending the confirmation email.')
                    return redirect('bookappointment')
            else:
                messages.error(request,'unsuccessful')
        else:
            form=Appointments()
    return render(request,'appointment/appointment_book.html',{'form':form,'departments':department,'date':date})

# @login_required(login_url='patientlogin')
def appointmentsuccess(request):
    return render(request,'appointment/appointment_success.html')

# @login_required(login_url='doctorlogin')
def viewappointments(request):
    appointments=Appointment.objects.all()
    pending=Appointment.objects.filter(status='pending')
    booked=Appointment.objects.filter(status='booked')
    context={'appointments':appointments,'pending':pending,'booked':booked}
    return render(request,'appointment/appointment_view.html',context)

# @login_required(login_url='doctorlogin')
def deleteappointment(request,pk):
    appointment = Appointment.objects.get(pk=pk)
    if request.method=='POST':
        appointment.delete()
        return redirect('doctordashboard')
    return render(request,'appointment/appointment_deleteconfirm.html',{'obj':appointment})

def appointmentlimit(request):
    return render(request,'appointment/appointment_limit.html')
# def appointmentapprove(request,pk):
    # appointment=Appointment.objects.all.get(pk=pk)
    # if request.method=='POST':
    #     appointment.status='Booked'

def get_doctors_by_department(request):
    department_id = request.GET.get('department_id')
    doctors = Doctorreg.objects.filter(department_id=department_id)
    return render(request, 'doctors_dropdown.html', {'doctors': doctors})
#-----------------------------------------------------------------
def reportform(request):
    if request.method=='POST':
        form=reports(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctorhome')
        else:
            messages.error(request,'unsuccessful')
    else:
        form=reports()
    return render(request,'doctor/report_form.html',{'form':form})



def report(request):
    q= request.GET.get('q','') if request.GET.get('q')!=None  else ''
    patient=Patientreg.objects.filter(Q(username__icontains=q))
    # doctor_count=doctor.count()
    # has_firstname = bool(q) and 'firstname' in q.lower()
    # topic=Depts.objects.all()
    report = ReportHistory.objects.filter(Q(patient__username__icontains=q))
    context={'patient':patient,'report':report}
    return render(request,'report.html',context) 

#--------EMAIL------------------------------------------------------------------------


# def send_email(request):
#     subject = 'Registration!'
#     message = 'Your registration into HOSPITAL MANAGEMENT SYSTEM is successful.Thank you!'
#     from_email = 'shaikrajiyasulthana13455@gmail.com'
#     recipient_list = ['shaikrajiyasulthana22@gmail.com']

#     send_mail(subject, message, from_email, recipient_list)

#----------DEPARTMENTS--------------------------------------------------------------------------------
def department(request,id):
    specialties = [
    {'id': 1, 'name': 'Cardiology', 'image': 'images/cardiology.webp'},
    {'id': 2, 'name': 'BMT', 'image': 'images/anesthesiologist.jpeg'},
    ]
    department = get_object_or_404(Departments, pk=id)
    doctors = Doctorreg.objects.filter(department=department)
    return render(request,'departments.html',{'department': department, 'doctors': doctors,'specialties':specialties})

# def hii(request):
#     username=request.user
#     doctor = Doctorreg.objects.get(username=username)
#     department = doctor.department
#     appointments = Appointment.objects.filter(department=department)
#     total = appointments.count()
#     doctor_id=doctor.id
#     context={'doctor_id':doctor_id,'appointment':appointments,'total':total}
#     return render(request,'hi.html',context)