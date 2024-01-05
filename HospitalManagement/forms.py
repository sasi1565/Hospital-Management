from django import forms
from .models import *
from django.forms import ModelForm

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        # fields = '__all__'
        # labels = {
        #     'firstname':'First Name',
        #     'lastname':'Last Name',
        #     'email':'Email',
        #     'phone':'Mobile Number',
        #     'age':'Age',
        #     'symptoms':'Symptoms',
        #     'department':'Department',
        #     'descrition':'Description',
        #     'date':'Appointment Date',
        # }
        # widgets = {
        #     'firstname':forms.TextInput(attrs={'class':'form-control'}),
        #     'lastname':forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     'phone':forms.NumberInput(attrs={'class':'form-control'}),
        #     'age':forms.NumberInput(attrs={'class':'form-control'}),
        #     'date':forms.DateInput(attrs={'class':'form-control'}),
        #     'symptoms':forms.TextInput(attrs={'class':'form-control'}),
        #     'department':forms.Select(attrs={'class':'form-select'}),
        #     'descrition':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        # }
        fields=['department']
        labels = {
            'department':'Department'
        }
        widgets = {
            'department' : forms.Select(attrs={'class':'form-select'})
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = patients
        fields=['department']
        labels = {
            'department':'Department'
        }
        widgets = {
            'department' : forms.Select(attrs={'class':'form-select'})
        }


class Approve_doctorForm(forms.ModelForm):
    class Meta:
        model = approve_doctors
        fields=['department']
        labels = {
            'department':'Department'
        }
        widgets = {
            'department' : forms.Select(attrs={'class':'form-select'})
        }

class DoctorregForm(forms.ModelForm):
    class Meta:
        model = Doctorreg
        fields=['department']
        labels = {
            'department':'Department'
        }
        widgets = {
            'department' : forms.Select(attrs={'class':'form-select'})
        }


#---------------------------------------

class DoctorForm1(forms.ModelForm):
    class Meta:
        model=approve_doctors
        fields=['firstname','lastname','username','age','email','address','mobile','department','experience','qualification']
        labels = {
            'firstname':'First Name',
            'lastname':'Last Name',
            'username':'Username',
            'age':'Age',
            'email':'Email',
            'address':'Address',
            'department':'Department',
            'experience':'Experience',
            'qualification':'Qualification',
        }
        widgets = {
            'firstname':forms.TextInput(attrs={'class':'form-control'}),
            'lastname':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-select'}),
            'experience':forms.NumberInput(attrs={'class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
        }
        experience=forms.IntegerField(
            min_value=0,
            max_value=60,
        )

# class DoctorForm2(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username','password1','password2']
#         exclude=['host']
class Appointments(forms.ModelForm):
    class Meta:
        model=Appointment  
        fields=['firstname','lastname','email','phone','age','symptoms','department','description']
        labels = {
            'firstname':'First Name',
            'lastname':'Last Name',
            'email':'Email',
            'age':'Age',
            'symptoms':'Symptoms',
            'department':'Department',
            'descrition':'Description',
            'gender':'Gender',
        }
        widgets = {
            'firstname':forms.TextInput(attrs={'class':'form-control'}),
            'lastname':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'class':'form-control'}),
            'symptoms':forms.TextInput(attrs={'class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-select'}),
            'descrition':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        }


class Patientregs(forms.ModelForm):
    class Meta:
        model=Patientreg
        fields=['username','email']
        labels = {
            'username':'Username',
            'email':'Email',
        }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class reports(forms.ModelForm):
    class Meta:
        model=ReportHistory
        fields='__all__'
        labels = {
            'patient':'Patient',
            'doctor':'Doctor',
            'report':'Report',
        }
        widgets = {
            'patient' : forms.Select(attrs={'class':'form-select'}),
            'doctor' : forms.Select(attrs={'class':'form-select'}),
            'report' : forms.FileInput(attrs={'class':'form-control'}),
        }

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}),label='Name')
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),label='Email')
    Message = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'class':'form-control'}),label='Message' )

