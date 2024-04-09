from django.db import models
from django.contrib.auth.models import User

class User_Details(models.Model):
	user_id=models.AutoField(db_index=True,primary_key=True)
	username = models.CharField(db_index=True, max_length=255, unique=True,blank=False)
	f_name=models.CharField(db_index=True,max_length=120)
	l_name=models.CharField(db_index=True,max_length=120,null=True)
	email=models.EmailField(db_index=True,null=True)
	password=models.CharField(db_index=True,max_length=120)
	mobile_no=models.IntegerField(db_index=True)
	dob=models.DateField(db_index=True)
	location=models.CharField(db_index=True,max_length=200)
	admin_user = models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		db_table = "User_Details"

class Account_Details(models.Model):
	user=models.ForeignKey(User_Details, on_delete=models.CASCADE)
	user_name=models.CharField(db_index=True,max_length=120)
	acc_no=models.IntegerField(db_index=True,primary_key=True)
	account_type=models.CharField(db_index=True,max_length=120)
	acc_balance= models.FloatField(db_index=True,blank=False)
	created_date=models.DateField()
	updated_at=models.DateTimeField(auto_now_add=True)
	acc_status=models.CharField(db_index=True,max_length=20,default='pending')

	class Meta:
		db_table = "Account_Details"


class Transaction_history(models.Model):
	transaction_id=models.AutoField(primary_key=True)
	user=models.ForeignKey(User_Details,on_delete=models.CASCADE)
	transaction_type=models.CharField(max_length=20)
	date=models.DateTimeField(auto_now_add=True)
	amount=models.DecimalField(max_digits=10,decimal_places=2)
	from_account=models.CharField(db_index=True,max_length=120)
	to_account=models.CharField(db_index=True,max_length=120)

	class Meta:
		db_table = "Transaction_history"

# Create your models here.
