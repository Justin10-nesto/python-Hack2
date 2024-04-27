from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from .models import *
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.db import transaction
import os
# Create your views here.

def random_date(start, end):
    delta = start - end
    int_delta = (delta.days*24*60*60)+delta.seconds
    random_seconds = random.randint(0, -int_delta)
    return start+timedelta(seconds=random_seconds)

@transaction.atomic()
def registerPage(request):
    if request.method == "POST":
        print('ok')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        bod = request.POST.get('bod')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        username = request.POST.get('username')
        if not email:
            registration_no = random.randint(0, 1000)
            email= first_name+last_name+registration_no +'@gmail.com'
            
        User.objects.create_user(username=username, email=email, password=password)
        user = User.objects.filter(username = username).first() 
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = True
        user.save()
        
        full_name = ''
        if middle_name:            
            full_name = first_name + ' ' + ' ' + last_name
        else:
            full_name = first_name + ' ' + middle_name + ' ' + last_name
        UserDetails.objects.create(full_name=full_name,  country = country, phone_number= phone_number, bod = bod, gender = gender, user = user)

        messages.success(request,'User account is created successful')
        Group.objects.get_or_create(name = 'Normal User')
        role = Group.objects.filter(name = 'Normal User').first()
        user.groups.add(role)
        return redirect('loginPage')

    context = {}
    return render(request, 'UAA/pages-register.html', context)

def loginPage(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user =authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_active:
                    messages.success(request,'User is successful logged in')
                    return redirect('DashboardPage')
                
                elif user.is_superuser:
                    return redirect('admin')
                else:
                    messages.error(request,'Account is blocked')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request,'Incorrect username or password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'UAA/pages-login.html')

def updateUser(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            file = request.FILES['file']
            phone_no = request.POST.get('phone_no')

            user_id = request.user.id
            user = User.objects.filter(id = user_id).first()
            User_info = UserDetails.objects.filter(user=user).first()
            User_info.phone_number = phone_no
            User_info.email = email
            User_info.photo = file
            User_info.save()
            messages.success(request,'User is deleted successful')

            return redirect('userProfilePage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def changePassword(request):
    try:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user_id = request.user.id
                user = User.objects.filter(id = user_id).first()
                user.set_password(password1)
                return redirect('userProfilePage')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def foggotenPassword(request):
    user = request.user
    if request.method == "POST":
        email = request.POST.get('username')
        is_user_exists = User.objects.filter(email=email).exists()
        opt_generated = ''
        status = True
        if is_user_exists:
            user = User.objects.filter(email=email).first()
            opt_objs = OtpCode.objects.filter(user = request.user)
            if opt_objs.exists():
                opt_obj = opt_objs.first()
                if opt_obj.get_status == 'Valid':
                    opt_generated = opt_obj.code
                    status = True
                else:
                    status = False
            else:
                status = False
            if not status:
                opt = random.randint(100000,999999)
                opt_generated = 'E-' + str(opt)
                OtpCode.objects.create(code = opt_generated, user = user)
            header = 'Resset Password'
            message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(header, message, email_from, [email])
            return redirect(f'../opt_sent/{user.id}')
    return render(request, 'UAA/foggotpassword.html')

def resend_password(request, id):
    user = User.objects.filter(id=id).first()
    otp = OtpCode.objects.filter(user = user).first()
    opt_generated =otp.code
    header = 'Resset Password'
    message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
    email_from = settings.EMAIL_HOST_USER
    email_to = otp.user.email
    send_mail(header, message, email_from, [email_to])
    return redirect(f'../opt_sent/{user.id}')

def opt_sent(request, id):
    if request.method == "POST":
        code = request.POST.get('code')
        user = User.objects.filter(id=id).first()
        opts = OtpCode.objects.filter(user = user)
        if opts.exists():
            for opt in opts:
                if opt.code == code:
                    if opt.get_status == 'Valid':
                        messages.error(request,'Code used has been arleady expired')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
                    else:
                        opt.is_used = True
                        opt.save()
                        return redirect(f'../setting_password/{user.id}')
                messages.error(request,'Incorrect code used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('foggotenPassword')

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/opt-sent.html', context)

def setting_password(request, id):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.filter(id=id).first()
            user.set_password(password1)
            messages.success(request,'Your password Account is reseted successfully')
            return redirect('loginPage')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/new-password.html', context)

def logoutPage(request):
    try:
        logout(request)
        return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def manageroles(request):
    roles_dict= []
    Roles = Group.objects.all().order_by('id')
    for role in Roles:
        permisions = role.permissions.all()
        roles_dict.append({'role':role, 'permissions':permisions})
        
    context = {'roles_dict':roles_dict}
    return render(request,'UAA/manageroles.html', context)

def addroles(request):
    p = Group()
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            permission = [x.name for x in Permission.objects.all()]
            s_id = []
            p.name=name
            for x in permission:
                    s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
            p.save()
            messages.success(request,'User is deleted successful')

            for s in s_id:
                p.permissions.add(Permission.objects.filter(id=s).first())
                p.save()
                messages.success(request,'User is deleted successful')

            messages.success(request,'Role added successful')
            return redirect('/manageroles')

        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        permission = Permission.objects.all()
        context = {'permission':permission}
        return render(request, 'UAA/add-role.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def RemoveRole(request, rid, pid):
    try:
        permission = Permission.objects.filter(id = pid).first()
        roles = Group.objects.filter(id = rid).first()
        roles.permissions.remove(permission)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def AssignUserRole(request, uid):
    user = User.objects.filter(id = uid).first()
    if request.method == 'POST':
        for j in user.groups.all():
            user.groups.remove(j)
        groups = [x.name for x in Group.objects.all()]

        s_id = []
        for x in groups:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        print(s_id)
        for s in s_id:
            user.groups.add(Group.objects.filter(id=s).first())
        messages.success(request,'roles are assigned to user successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def editroles(request,id):
    exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
    p = Permission.objects.exclude(id__in=exclude_perm)
    r = Group.objects.filter(id=id)
    y=Group.objects.filter(id=id).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        for j in Permission.objects.all():
            y.permissions.remove(j)
        permission = [x.name for x in Permission.objects.all()]

        s_id = []
        Group.objects.filter(id=id)
        for x in permission:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        r=Group.objects.filter(id=id).update(name=name)

        for s in s_id:
            y.permissions.add(Permission.objects.get(id=s))
        messages.success(request,'permissions are added successful')
        return redirect('/manageroles')

    role = Group.objects.filter(id = id).first()
    permission = Permission.objects.all()
    context = {'permission':permission, 'role':role}
    return render(request, 'UAA/edit-role.html', context)

@login_required(login_url='/login')
def blockuser(request,id):
      try:
        u = User.objects.filter(id=id).filter(is_active='True').exists()
        if u:
            User.objects.filter(id=id).update(is_active='False')
            messages.success(request,'block successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            User.objects.filter(id=id).update(is_active='True')
            messages.success(request,'Activation successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def deleteroles(request,id):
    g = Group.objects.filter(id=id).delete()
    messages.success(request,'User is deleted successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def userProfilePage(request):
    return render(request, 'UAA/profile.html')

def userList(request):
    User_list = []
    users = []
    user =User.objects.filter(id = request.user.id).first()
    User_list = UserDetails.objects.all()
    users = User.objects.all()
    groups_list = Group.objects.all()

    users_groups = []
    if users:
        for user in users:
            groups = user.groups.all()
            users_groups.append({'user':user, 'groups':groups})
    context = {'users_groups':users_groups, 'User_list':User_list, 'groups_list':groups_list}

    return render(request, 'UAA/UserList.html', context)

def DashboardPage(request):
    context = {}
    return render(request, 'Admin/dashboard.html', context)
