from django.urls import path, include
from . import views
urlpatterns = [
    
    path('', views.loginPage, name='loginPage'),
    path("logoutPage", views.logoutPage, name="logoutPage"),
    path('register', views.registerPage, name ='registerPage'),
    path('foggotenPassword', views.foggotenPassword, name= 'foggotenPassword'),
    path('opt_sent/<str:id>', views.opt_sent, name= 'opt_sent'),
    path('resend_password/<str:id>', views.resend_password, name= 'resend_password'),
    path('setting_password/<str:id>', views.setting_password, name= 'setting_password'),

    path('manageroles', views.manageroles, name ='manageroles'),
    path('addroles', views.addroles, name ='addroles'),
    path('RemoveRole/<str:rid>/<str:pid>', views.RemoveRole, name ='RemoveRole'),
    path('AssignUserRole/<str:uid>', views.AssignUserRole, name ='AssignUserRole'),
    path('editroles/<str:id>', views.editroles, name ='editroles'),
    path('deleteroles/<str:id>', views.deleteroles, name ='deleteroles'),

    path('blockuser/<str:id>', views.blockuser, name ='blockuser'),
    path('userList', views.userList, name ='userList'),
    path('userProfile', views.userProfilePage, name ='userProfilePage'),
    path('changePassword', views.changePassword, name = 'changePassword'),
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),

]
