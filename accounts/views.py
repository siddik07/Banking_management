from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserForm
from datetime import datetime
from django.db import transaction
import random as r
from django.contrib.auth.decorators import login_required



def send_mail_to_user(subject,message,recipient_mail):
    print("email in")
    from_mail=settings.EMAIL_HOST_USER
    send_mail(subject,message,from_mail,recipient_mail,fail_silently=False,)
    print("email sent")


def home(request):
	return render(request,'index.html')

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
            if user is not None:
                print(5)
                admin=User.objects.filter(id=user.id).first()
                if admin.is_superuser==1:
                	login(request,user)
                	print("login")
                	return redirect('admindash')
                else:
                	messages.error(request,'Username or Password Does not match')  
                	return redirect('adminlogin')           	
        except:
            messages.error(request,'Username or Password Does not match')
            return redirect ('adminlogin')   
    return render(request,'adminLogin.html')

#adminlogout
def adminLogout(request):
	logout(request)
	return redirect('adminlogin')

# userregisterpage
def userRegister(request):
	if request.method=='POST':
		form=CustomUserForm(request.POST)
		data = request.POST
		fname=data.get('fname')
		lname=data.get('lname')
		username=data.get('username')
		email=data.get('email')
		password2=data.get('password2')
		mobileno=data.get('mobile')
		dob=data.get('dob')
		location=data.get('place')
		account_type=data.get('acctyp')
		acc_balance=data.get('deposit')
		if form.is_valid():
			print("form valid success")
			form.save()
			admin_user = User.objects.filter(username=username).first()
			admin_user_id=admin_user.id 
			userdetail=User_Details(f_name=fname,l_name=lname,username=username,
				email=email,password=password2,mobile_no=mobileno,
				dob=dob,location=location,admin_user_id=admin_user_id)
			userdetail.save()
			users = User_Details.objects.filter(username=username).first()
			user_id=users.user_id
			user_name=users.username
			accno=r.randint(2673879809,7464301754)
			print(accno)
			date = datetime.now().date()
			acc_detail=Account_Details(user_name=user_name,acc_no=accno,account_type=account_type,
                                        acc_balance=acc_balance,created_date=date,user_id=user_id)
			acc_detail.save()
			transhistory=Transaction_history(transaction_type="first self deposit ",amount=acc_balance,
										from_account_user=user_name,to_account_user=user_name,
										from_account_no=accno,to_account_no=accno,
										user_id=user_id)
			transhistory.save()	
			subject="Account Information"
			message=f"hi, {userdetail.username}.You are successfully created account with Account_No {acc_detail.acc_no} in our bank but still pending.Please wait our manger will activate your account"
			to_mail=[users.email]
			send_mail_to_user(subject,message,to_mail)
			return redirect('userlogin')

		else:
			print("form not valid")

	else:	
		form=CustomUserForm()
		print(form)
		# form.fields['username'].widget.attrs['placeholder']='Enter username'
		# # form.fields['email'].widget.attrs['placeholder']='Enter Email'
		# form.fields['password1'].widget.attrs['placeholder']='Enter Password'
		# form.fields['password2'].widget.attrs['placeholder']='Conform Password'
		return render(request,'userreg.html',{'form':form})



# userloginpage
def userLogin(request):
	if request.method == 'POST':
		name=request.POST.get('username')
		pwd=request.POST.get('password')
		print(name)
		print(pwd)
		try:
			user=authenticate(request,username=name,password=pwd)
			print(user)
			print(4)
			if user is not None:
				print(5)
				login(request,user)
				print("login")
				user_id=request.user.id 
				account=Account_Details.objects.filter(user_id=user_id).first()
				print(account)
				if account.acc_status == 'active':
					return redirect('userdash',account.user_id)
				elif account.acc_status == 'block':
					print("Blocked")
					messages.error(request,'Your Account has been Blocked,Please contact manager or admin')
					return redirect('userlogin')					
				else:
					print("not activated")
					messages.error(request,'Your Account is not activated,Please contact manager or admin')
					return redirect('userlogin') 
		except:
			print('except block')
			messages.error(request,'Username or Password Does not match')
			return redirect('userlogin')

	return render(request,'userlogin.html')	

#userlogout
def userLogout(request):
	logout(request)
	return redirect('userlogin')

#forgetPassword
def pwdReset(request):
	if request.method=='POST':
		print("come")
		accno=request.POST.get('accno')
		Account=Account_Details.objects.filter(acc_no=accno).first() 
		print(Account)
		if Account is None:
			messages.error(request,'Account No is Invalid,Enter Correct Account No..')
			return redirect('pwdreset')
		else:
			return redirect('password_reset')	
	else:
		return render(request,'pwdreset.html')


# userDash
def userDash(request,pk):
	acc_user=Account_Details.objects.filter(user_id=pk).first()
	print(acc_user.user_name)
	return render(request,'userdash.html',{'acc_user':acc_user})


# AdminDash
@login_required(login_url='adminlogin')
def adminDash(request):
    user_account=Account_Details.objects.all()
    admin=User.objects.filter(is_superuser=1).first()
    context={'user_account':user_account,'admin':admin}
    return render(request,'admindash.html',context)

# adminAction
@login_required(login_url='adminlogin')
def adminAction(request,pk):
    user_data1=User_Details.objects.filter(user_id=pk).values()
    user_data2=Account_Details.objects.filter(user_id=pk).values()
    context={'user_data1':user_data1,'user_data2':user_data2}
    return render(request,'userdetails.html',context)

def userActive(request,pk):
    user_acc=Account_Details.objects.filter(user_id=pk).first()
    if user_acc.acc_status=='active':
    	messages.success(request,'This user account has been already Activated')
    	return redirect('adminaction',pk)
    else:	
	    user_acc.acc_status='active'
	    user_acc.save()
	    userdetail=User_Details.objects.filter(user_id=pk).first()
	    subject="Account Activated"
	    message=f"hi {userdetail.username}.Your Account has been Activated by our admin in Our Bank.Now you can use Our Banking services by logging in your account."
	    to_mail=[userdetail.email]
	    send_mail_to_user(subject,message,to_mail)
	    messages.success(request,'This User Account has been Activated')
	    return redirect('adminaction',pk)



def userBlock(request,pk):
    user_acc=Account_Details.objects.filter(user_id=pk).first()
    if user_acc.acc_status=='block':
    	messages.success(request,'This user account has been already Blocked')
    	return redirect('adminaction',pk)
    else:
	    user_acc.acc_status='block'
	    user_acc.save()
	    messages.success(request,'This User Account has been Blocked')
	    return redirect('adminaction',pk)


def userEdit(request,pk):
	if request.method=='POST':
		print("come")
		data = request.POST
		username=data.get('username')
		fname=data.get('fname')
		lname=data.get('lname')
		email=data.get('email')
		mobileno=data.get('mobile')
		location=data.get('place')
		userdetail=User_Details.objects.filter(user_id=pk).first()
		userdetail.username=username
		userdetail.f_name=fname
		userdetail.l_name=lname
		userdetail.email=email
		userdetail.mobile_no=mobileno
		# userdetail.dob=dob
		userdetail.location=location
		userdetail.save()
		date = datetime.now().date()
		user_acdet=Account_Details.objects.filter(user_id=pk).first()
		# user_acdet.updated_at=date
		user_acdet.save()
		print("updated")
	else:
		userdet=User_Details.objects.filter(user_id=pk).values()
		print(userdet)
		return render(request,'userdetailedit.html',{'userdet':userdet})	
		
# balancecheck
@login_required(login_url='userlogin')
def balanceCheck(request,pk):
	balance=Account_Details.objects.filter(user_id=pk).first()
	bal_amt=balance.acc_balance
	messages.info(request,f"Your Account Balance is {bal_amt}")
	return redirect('userdash',pk)

# deposit
@transaction.atomic()
@login_required(login_url='userlogin')
def deposit(request,pk):
	if request.method=='POST':
		data=request.POST
		amount=data.get('amt')
		amount=float(amount)
		account=Account_Details.objects.filter(user_id=pk).first()
		account.acc_balance+=amount
		account.save()
		transhistory=Transaction_history(transaction_type="self deposit",amount=amount,
										from_account_user=account.user_name,to_account_user=account.user_name,
										from_account_no=account.acc_no,to_account_no=account.acc_no,
										user_id=account.user_id)
		transhistory.save()
		print("success")
		messages.info(request,"successfully Amount Deposited in your Bank Account")
		messages.info(request,f"Your Balance is {account.acc_balance}")
		return redirect('deposit',pk)
	else:
		userdet=User_Details.objects.filter(user_id=pk).first()
		return render(request,'deposit.html',{'userdet':userdet})	

#withdrawPage
@transaction.atomic()
@login_required(login_url='userlogin')
def withdraw(request,pk):
	if request.method=='POST':
		data=request.POST
		amount=data.get('amt')
		amount=float(amount)
		account=Account_Details.objects.filter(user_id=pk).first()
		account.acc_balance-=amount
		account.save()
		transhistory=Transaction_history(transaction_type="self withdraw",amount=amount,
										from_account_user=account.user_name,to_account_user=account.user_name,
										from_account_no=account.acc_no,to_account_no=account.acc_no,
										user_id=account.user_id)
		transhistory.save()
		print("success")
		messages.info(request,"Successfully Amount Withdraw in your Bank Account")
		messages.info(request,f"Your Balance is {account.acc_balance}")
		return redirect('withdraw',pk)
	else:
		userdet=User_Details.objects.filter(user_id=pk).first()
		return render(request,'withdraw.html',{'userdet':userdet})	

#moneyTransferPage
@transaction.atomic()
@login_required(login_url='userlogin')
def moneyTransfer(request,pk):
	if request.method=='POST':
		data=request.POST
		from_ac=data.get('fromaccno')
		to_ac=data.get('toaccno')
		amount=data.get('amt')
		remark=data.get('remark')
		amount=float(amount)
		accountdet=Account_Details.objects.values('acc_no')
		for i in accountdet:
			if int(to_ac)==i['acc_no']:
				from_acdet=Account_Details.objects.filter(acc_no=from_ac).first()
				to_acdet=Account_Details.objects.filter(acc_no=to_ac).first()
				from_acdet.acc_balance-=amount
				to_acdet.acc_balance+=amount
				from_acdet.save()
				to_acdet.save()
				transhistory=Transaction_history(transaction_type="self transfer",amount=amount,
										from_account_user=from_acdet.user_name,to_account_user=to_acdet.user_name,
										from_account_no=from_acdet.acc_no,to_account_no=to_acdet.acc_no,
										user_id=from_acdet.user_id)
				transhistory.save()
				messages.info(request,f"Successfully Amount Transfered  {to_acdet.user_name} Bank Account")
				return redirect('transfer',pk)
			else:
				messages.error(request,f"{to_ac} Account No not Found")	
				messages.error(request,"Please Enter Correct Sender Account Number")
				return redirect('transfer',pk)		
	else:
		userdet=Account_Details.objects.filter(user_id=pk).first()
		return render(request,'moneytransfer.html',{'userdet':userdet})	

#userStatement
@login_required(login_url='userlogin')
def userStatements(request,pk):
	useracc=Account_Details.objects.filter(user_id=pk).first()
	statements=Transaction_history.objects.filter(user_id=pk)
	if request.method =='POST':
		Id=request.POST.get('id')
		date=request.POST.get('date')
		print(date)
		if Id == '':
			statements=Transaction_history.objects.filter(date__contains=date,user_id=pk).values()
			print(statements)
			print("work")
		elif date =='':	
			statements=Transaction_history.objects.filter(transaction_id=Id,user_id=pk).values()
			print(statements)
		elif Id != '' and date !='':
			statements=Transaction_history.objects.filter(transaction_id=Id,date__contains=date,user_id=pk).values()
		if statements == []:
			messages.error(request,'No Records Found')
			print("work")
			return redirect('userstatements',pk)				
	return render(request,'statement.html',{'statements':statements,'useracc':useracc})


#adminpageuserstatements
@login_required(login_url='adminlogin')
def adminUserStatements(request):
	statements=Transaction_history.objects.all()
	return render(request,'transactions.html',{'statements':statements})

# particularuserstatements
@login_required(login_url='adminlogin')
def particularUserStatements(request,pk):
	useracc=Account_Details.objects.filter(user_id=pk).first()
	statements=Transaction_history.objects.filter(user_id=pk)
	if request.method =='POST':
		Id=request.POST.get('id')
		date=request.POST.get('date')
		print(date)
		if Id == '':
			statements=Transaction_history.objects.filter(date__contains=date,user_id=pk).values()
			print(statements)
			print("work")
		elif date =='':	
			statements=Transaction_history.objects.filter(transaction_id=Id,user_id=pk).values()
			print(statements)
		elif Id != '' and date !='':
			statements=Transaction_history.objects.filter(transaction_id=Id,date__contains=date,user_id=pk).values()
		if statements == []:
			messages.error(request,'No Records Found')
			print("work")
			return redirect('userstatements',pk)				
	return render(request,'particularstatement.html',{'statements':statements,'useracc':useracc})



