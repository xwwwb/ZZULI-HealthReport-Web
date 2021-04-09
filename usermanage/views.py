from django.shortcuts import render, redirect
from .froms import UserForm, RegisterForm
from usermanage import models
import hashlib


# Create your views here.

def hash_code(s, salt='xwwwb'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def checkpassword(password):
    length = len(password)
    if (length < 6):
        return 0
    else:
        return 1


def index(request):
    return render(request, 'usermanage/index.html')


# def login(request): //使用models
#     if(request.method=='POST'):
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         print(password,username)
#         message = "所有字段都必须填写！"
#         username = username.strip()
#         try:
#             user=models.User.objects.get(name=username)
#             if user.password == password:
#                 return redirect('/index/')
#             else:
#                 message = "密码不正确！"
#         except:
#             message="用户名不存在"
#         return render(request, 'usermanage/login.html',{"message": message})
#     return render(request,'usermanage/login.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    if (request.method == 'POST'):
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        print(useremail, password)
        message = "请检查填写的内容"
        try:
            user = models.User.objects.get(email=useremail)
            print(1)
            if (user.password == hash_code(password)):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = "密码错误"
        except:
            message = "此邮箱不存在"
        return render(request, 'usermanage/signin.html', context={'message': message})
    return render(request, 'usermanage/signin.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if (request.method == "POST"):
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if (password1 != password2):
                message = "两次输入的密码不同"
                return render(request, 'usermanage/register.html',
                              context={'register_form': register_form, 'message': message})
            else:
                if (checkpassword(password1)):
                    samenameuser = models.User.objects.filter(name=username)
                    if samenameuser:
                        message = "用户名已存在，请重新选择用户名"
                        return render(request, 'usermanage/register.html',
                                      context={'register_form': register_form, 'message': message})
                    sameemail = models.User.objects.filter(email=email)
                    if sameemail:
                        message = "该邮箱已被注册，请使用其他邮箱"
                        return render(request, 'usermanage/register.html',
                                      context={'register_form': register_form, 'message': message})
                else:
                    message = "密码长度大于6"
                    return render(request, 'usermanage/register.html',
                                  context={'register_form': register_form, 'message': message})
            new_user = models.User.objects.create()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.save()
            message = "注册成功，请登录"
            return redirect('/login/', context={'message': message})
    register_form = RegisterForm()
    return render(request, 'usermanage/register.html', context={'register_form': register_form, })


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')


def editpassword(request):
    if not request.session.get('is_login', None):
        message = "请先登录，即将为您跳转到登录页"
        return render(request, 'usermanage/editpassword.html', context={'message': message})

    if (request.method == "POST"):
        userid = request.session['user_id']
        edit_userpassw = models.User.objects.get(id=userid)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        password3 = request.POST.get("password3")
        if (edit_userpassw.password == hash_code(password1)):
            if (password2 != password3):
                message = "两次输入密码不相同，请重试!"
                return render(request, 'usermanage/editpassword.html', context={'message': message})
            else:
                if(checkpassword(password2)):
                    edit_userpassw = models.User.objects.get(id=userid)
                    edit_userpassw.password = hash_code(password2)
                    edit_userpassw.save()
                    message = "更新密码成功，5秒后自动登出，请重新登录"
                    return render(request, 'usermanage/editpassword.html', context={'message': message})
                else:
                    message="密码长度大于6"
                    return render(request, 'usermanage/editpassword.html', context={'message': message})
        else:
            message = "目前的密码不正确，请检查后再试"
            return render(request, 'usermanage/editpassword.html', context={'message': message})
    return render(request, 'usermanage/editpassword.html')
