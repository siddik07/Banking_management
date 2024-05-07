from django.urls import path
from .import views 

urlpatterns = [
	path('',views.home,name='home'),
	path('adminlogin',views.adminLogin,name='adminlogin'),
	path('adminlogout',views.adminLogout,name='adminlogout'),
	path('userlogin',views.userLogin,name='userlogin'),
	path('userlogout',views.userLogout,name='userlogout'),
	path('userreg',views.userRegister,name='userreg'),
	path('admindash',views.adminDash,name='admindash'),
	path('adminaction/<pk>',views.adminAction,name='adminaction'),
	path('activateuser/<pk>',views.userActive,name='activateuser'),
    path('blockuser/<pk>',views.userBlock,name='blockuser'),
    path('useredit/<pk>',views.userEdit,name='useredit'),
    path('userdash/<pk>',views.userDash,name='userdash'),
    path('balance/<pk>',views.balanceCheck,name='balance'),
    path('deposit/<pk>',views.deposit,name='deposit'),
    path('withdraw/<pk>',views.withdraw,name='withdraw'),
    path('transfer/<pk>',views.moneyTransfer,name='transfer'),
    path('userstatements/<pk>',views.userStatements,name='userstatements'),
    path('adminuserstatements',views.adminUserStatements,name='adminuserstatements'),
    path('particularstatements/<pk>',views.particularUserStatements,name='particularstatements'),

]