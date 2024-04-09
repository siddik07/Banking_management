from django.urls import path
from .import views 

urlpatterns = [
    path('',views.index,name=''),
    path('userlogin',views.userLogin,name='userlogin'),
    path('adminlogin',views.adminLogin,name='adminlogin'),
    path('admindash',views.adminDash,name='admindash'),
    path('userreg',views.userRegister,name='userreg'),
    path('adminaction/<pk>',views.adminAction,name='adminaction'),
    path('activateuser/<pk>',views.userActive,name='activateuser'),
    path('blockuser/<pk>',views.userBlock,name='blockuser'),
]
