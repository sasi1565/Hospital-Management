from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.utils import timezone

class Doctorreg(models.Model):
    doctor_id=models.IntegerField(default=1000,primary_key=True)
    firstname=models.CharField(default=None,max_length=40,null=True)
    lastname=models.CharField(null=True,max_length=40,default=None)
    username = models.CharField(max_length=100,unique=True,null=True)
    email=models.EmailField(null=True,default=None)
    experience=models.IntegerField(null=True,default=None)
    image = models.ImageField(upload_to='images/',null=True,default='null')
    gender=models.CharField(null=True,max_length=10,default='Male')
    age=models.IntegerField(default=None,null=True)
    date=models.CharField(null=True,max_length=20,default=None)
    password=models.CharField(max_length=20,null=True)
    department=models.ForeignKey('Departments',on_delete=models.SET_NULL,null=True)
    qualification=models.CharField(null=True,max_length=40,default=None)
    mobile=models.IntegerField(null=True,default=None)
    address=models.CharField(max_length=50,null=True,default=None)
    def __str__(self):
        return f'Dr.{self.firstname} {self.lastname}'

class approve_doctors(models.Model):
    firstname=models.CharField(null=True,max_length=40)
    lastname=models.CharField(null=True,max_length=40)
    username = models.CharField(max_length=100,unique=True,null=True)
    email=models.EmailField(null=True,default=None)
    experience=models.IntegerField(null=True,default=None)
    gender=models.CharField(null=True,max_length=10,default='Male')
    image = models.ImageField(upload_to='images/',null=True,default='null')
    date=models.CharField(null=True,max_length=20)
    qualification=models.CharField(null=True,max_length=40,default=None)
    age=models.IntegerField(null=True,default=None)
    password=models.CharField(null=True,max_length=20)
    department=models.ForeignKey('Departments',on_delete=models.SET_NULL,null=True)
    mobile=models.IntegerField(null=True,default=None)
    address=models.CharField(max_length=50,null=True)
    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    

class feedback_data(models.Model):
    name=models.CharField(default='Null',max_length=40)
    email=models.EmailField()
    message=models.CharField(max_length=400)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    firstname = models.CharField(max_length=255,null=True)
    lastname = models.CharField(max_length=255,null=True)
    email=models.EmailField(max_length=254,null=True)
    gender=models.CharField(null=True,max_length=10,default='Male')
    phone = models.CharField(max_length=10,null=True)
    age=models.CharField(max_length=3,null=True)
    date=models.CharField(max_length=30,null=True)
    symptoms=models.CharField(max_length=400,null=True)
    department=models.ForeignKey('Departments',on_delete=models.SET_NULL,null=True)
    doctor=models.ForeignKey('Doctorreg',null=True,default=None,on_delete=models.SET_NULL)
    description=models.TextField(max_length=200,null=True)
    def __str__(self):
        return self.firstname

class patients(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    mobileno = models.IntegerField(null=True)
    age = models.IntegerField(default=0)
    gender=models.CharField(null=True,max_length=10,default='Male')
    image = models.ImageField(upload_to='images/',null=True,default='null')
    app_date = models.CharField(default=timezone.now().date().strftime("%Y-%m-%d"),max_length=20)
    doctor=models.ForeignKey('Doctorreg',null=True,default=None,on_delete=models.SET_NULL)
    symptoms = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    department = models.ForeignKey('Departments',on_delete=models.SET_NULL,null=True) 
    description = models.CharField(max_length=100,null=True,default='null')
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class admins(models.Model):
    admin_id=models.CharField(default=0,primary_key=True,max_length=10)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    def __str__(self):  
        return self.username

class Departments(models.Model):
    department=models.CharField(max_length=70,default="Cardiologist",null=True,)
    def __str__(self):
        return self.department

class discharged_patients(models.Model):
    discharge_id = models.IntegerField(primary_key=True,default=None)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    mobileno = models.IntegerField()
    age = models.IntegerField(default=0)
    gender=models.CharField(null=True,max_length=10,default='Male')
    app_date = models.CharField(default=timezone.now().date().strftime("%Y-%m-%d"),max_length=20)
    dis_date=models.CharField(default=timezone.now().date().strftime("%Y-%m-%d"),max_length=20)
    symptoms = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True,default='null')
    app_or_pat=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

# class sample(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     image=models.ImageField(null=True)
class Patientreg(models.Model):
    username=models.CharField(max_length=100,unique=True,null=True)
    email=models.EmailField(max_length=254,null=True,unique=True)
    password= models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.username

class ReportHistory(models.Model):
    patient = models.ForeignKey(Patientreg,on_delete=models.CASCADE,null=True)
    report = models.FileField(upload_to='media/', null=True, blank=True)
    date=models.DateField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        if self.patient:
            return f"Report for {self.patient}"
        else:
            return f"Report {self.pk}"
    
