from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .form import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from datetime import datetime
# from django.db import transaction
import random as r


# Create your views here.

def send_mail_to_user(subject,message,recipient_mail):
    print("email in")
    from_mail=settings.EMAIL_HOST_USER
    send_mail(subject,message,from_mail,recipient_mail,fail_silently=False,)
    print("email sent")


def index(request):
	return render(request,'index.html')

# userregisterpage
def userRegister(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        data = request.POST
        fname=data.get('fname')
        lname=data.get('lname')
        username=data.get('username')
        email=data.get('email')
        password1=data.get('password1')
        password2=data.get('password2')
        mobile_no=data.get('mobile')
        dob=data.get('dob')
        location=data.get('place')
        account_type=data.get('acctyp')
        acc_balance=data.get('deposit')
        if form.is_valid():
            print('form validation success')
            form.save()
            admin_user = User.objects.filter(username=username).first()

            userdetail=User_Details(f_name=fname,l_name=lname,username=username,email=email,
                                    password=password2,mobile_no=mobile_no,dob=dob,
                                    location=location,admin_user_id=admin_user.id)
            userdetail.save()
            users = User_Details.objects.filter(email=email).first()
            userid=users.user_id
            user_name=users.username
            accno=r.randint(26738798,74643017)
            print(accno)
            date = datetime.now().date()
            acc_detail=Account_Details(user_name=user_name,acc_no=accno,account_type=account_type,
                                        acc_balance=acc_balance,created_date=date,user_id=userid)
            acc_detail.save()
            subject="Account Confirmation"
            message=f"hi, {userdetail.username}.You are successfully created account with Account_No {acc_detail.acc_no} in our bank but still pending.Please wait our manger will activate your account"
            to_mail=[users.email]
            send_mail_to_user(subject,message,to_mail)
            print("saved")
            return redirect("userlogin")

        else:
            print("form not valid")

    return render(request,'userReg.html',{'form':form})


# userloginpage
def userLogin(request):
    if request.method == 'POST':
        print("post come")
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        print(name)
        print(pwd)
        try:
            user=authenticate(request,username=name,password=pwd)
            print(user)
            if user is not None:
                print(2)
                login(request,user)
                print(3)
                user_id = request.user.id
            acc=User_Details.objects.filter(admin_user_id=user_id).first()
            acc_id=acc.user_id
            acc_user=Account_Details.objects.filter(user_id=acc_id).first()
            print(acc_user)
            if acc_user.acc_status!= 'pending' or 'Block':
                return render(request,'userdash.html')
            else:
                print("not acivated")
                messages.error(request,'Your account is not acivated,Please contact admin')
                return redirect('userlogin')    
        except:
            messages.error(request,'Username or Password Does not match')
            return redirect ('userlogin')      
    return render(request,'userLogin.html')


#adminloginpage
def adminLogin(request):
    if request.method=='POST':
        print(2) 
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        print(name)
        print(pwd)
        try:
            print(3)
            user=authenticate(request,username=name,password=pwd)
            print(user)
            print(4)
            if user is not None:
                print(5)
                login(request,user)
                print(6)
                return redirect('admindash')
        except:
            messages.error(request,'Username or Password Does not match')
            return redirect ('adminlogin')   
    return render(request,'adminLogin.html')




# AdminDash
def adminDash(request):
    user_account=Account_Details.objects.all()
    context={'user_account':user_account}
    return render(request,'admindash.html',context)


# adminAction
def adminAction(request,pk):
    user_data1=User_Details.objects.filter(user_id=pk).values()
    user_data2=Account_Details.objects.filter(user_id=pk).values()
    context={'user_data1':user_data1,'user_data2':user_data2}
    return render(request,'user-details.html',context)


def userActive(request,pk):
    user_acc=Account_Details.objects.filter(user_id=pk).first()
    user_acc.acc_status='Active'
    user_acc.save()
    userdetail=User_Details.objects.filter(user_id=pk).first()
    subject="Account Activated"
    message=f"hi {userdetail.username}.Your Account has been Activated by our admin in Our Bank.Now you can use Our Banking services by logging in your account."
    to_mail=[userdetail.email]
    send_mail_to_user(subject,message,to_mail)
    messages.success(request,'This user account has been activated')
    return redirect('adminaction',pk)



def userBlock(request,pk):
    user_acc=Account_Details.objects.filter(user_id=pk).first()
    user_acc.acc_status='Block'
    user_acc.save()
    return redirect('adminaction')
