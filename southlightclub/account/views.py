from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout as auth_logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import PasswordForm


def login(request):
    template = 'account/login.html'
    if request.method=='GET':
        return render(request, template)
    #post
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        messages.error(request, '請輸入資料')
        return render(request, template)
    user = authenticate(username=username, password=password)
    if not user:
        messages.error(request, '登入失敗')
        return render(request, template)
    # user
    auth_login(request, user)
    messages.success(request, '登入成功')
    return redirect('admin:admin')


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '登出成功')
    return redirect('/')


@login_required
def accountUpdate(request):
    admin = get_object_or_404(User, username='admin')
    template = 'account/accountUpdate.html'
    if request.method=='GET':
        return render(request, template, {'passwordForm':PasswordForm(instance=request.user)})
    
    passwordForm = PasswordForm(request.POST, instance=request.user)
    if not passwordForm.is_valid():
        return render(request, template, {'passwordForm':passwordForm})
    
    admin.set_password(request.POST.get('password'))
    admin.save()
    messages.success(request, '修改成功')
    return redirect(reverse('admin:admin'))

