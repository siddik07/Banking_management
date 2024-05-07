from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class User_Details(models.Model):
	user_id=models.AutoField(db_index=True,primary_key=True)
	username = models.CharField(db_index=True, max_length=255, unique=True,blank=False)
	f_name=models.CharField(db_index=True,max_length=120)
	l_name=models.CharField(db_index=True,max_length=120,null=True)
	email=models.EmailField(db_index=True,null=True)
	password=models.CharField(db_index=True,max_length=120)
	mobile_no=models.BigIntegerField(db_index=True,validators=[MinValueValidator(1000000000),MaxValueValidator(999999999999999)])
	dob=models.DateField(db_index=True)
	location=models.CharField(db_index=True,max_length=200)
	admin_user = models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		db_table = "User_Details"

class Account_Details(models.Model):
	user=models.ForeignKey(User_Details, on_delete=models.CASCADE)
	user_name=models.CharField(db_index=True,max_length=120)
	acc_no=models.BigIntegerField(db_index=True,primary_key=True,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999999)])
	account_type=models.CharField(db_index=True,max_length=120)
	acc_balance= models.FloatField(db_index=True,blank=False,validators=[MinValueValidator(0),MaxValueValidator(9999999999999999)])
	created_date=models.DateField()
	updated_at=models.DateTimeField(auto_now_add=True)
	acc_status=models.CharField(db_index=True,max_length=20,default='pending')

	class Meta:
		db_table = "Account_Details"


class Transaction_history(models.Model):
	transaction_id=models.AutoField(primary_key=True)
	user=models.ForeignKey(User_Details,on_delete=models.CASCADE)
	transaction_type=models.CharField(max_length=50)
	date=models.DateTimeField(auto_now_add=True)
	amount=models.FloatField(db_index=True,validators=[MinValueValidator(0),MaxValueValidator(999999999999999)])
	from_account_user=models.CharField(db_index=True,max_length=120)
	from_account_no=models.BigIntegerField(db_index=True,default=0000000000,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999999)])
	to_account_user=models.CharField(db_index=True,max_length=120)
	to_account_no=models.BigIntegerField(db_index=True,default=0000000000,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999999)])
	remarks=models.CharField(db_index=True,max_length=120,default='others')

	class Meta:
		db_table = "Transaction_history"


