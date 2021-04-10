from django.shortcuts import render, redirect
# from .froms import UserForm, RegisterForm
from usermanage import models
from usermanage.function import hash_code,genrandom,sendcheckemail,checkpassword
# Create your views here.

def index(request):
    return render(request, 'usermanage/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(email=useremail)
            if user.password == hash_code(password):
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
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        if password1 != password2:
            message = "两次输入的密码不同"
            return render(request, 'usermanage/register.html',
                          context={'message': message})
        else:
            if checkpassword(password1):
                samenameuser = models.User.objects.filter(name=username)
                if samenameuser:
                    message = "用户名已存在，请重新选择用户名"
                    return render(request, 'usermanage/register.html',
                                  context={'message': message})
                sameemail = models.User.objects.filter(email=email)
                if sameemail:
                    message = "该邮箱已被注册，请使用其他邮箱"
                    return render(request, 'usermanage/register.html',
                                  context={'message': message})
            else:
                message = "密码长度大于6"
                return render(request, 'usermanage/register.html',
                              context={'message': message})
        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = hash_code(password1)
        new_user.email = email
        new_user.save()
        message = "注册成功！即将为您跳转到登录页"
        return render(request, 'usermanage/register.html', context={'message': message, 'check': 'success'})

    return render(request, 'usermanage/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')


def editpassword(request):
    if not request.session.get('is_login', None):
        message = "请先登录，即将为您跳转到登录页"
        return render(request, 'usermanage/editpassword.html', context={'message': message})

    if request.method == "POST":
        userid = request.session['user_id']
        edit_userpassw = models.User.objects.get(id=userid)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        password3 = request.POST.get("password3")
        if (edit_userpassw.password == hash_code(password1)):
            if password2 != password3:
                message = "两次输入密码不相同，请重试!"
                return render(request, 'usermanage/editpassword.html', context={'message': message})
            else:
                if checkpassword(password2):
                    edit_userpassw = models.User.objects.get(id=userid)
                    edit_userpassw.password = hash_code(password2)
                    edit_userpassw.save()
                    message = "更新密码成功，5秒后自动登出，请重新登录"
                    return render(request, 'usermanage/editpassword.html', context={'message': message})
                else:
                    message = "密码长度大于6"
                    return render(request, 'usermanage/editpassword.html', context={'message': message})
        else:
            message = "当前的密码不正确，请检查后再试"
            return render(request, 'usermanage/editpassword.html', context={'message': message})
    return render(request, 'usermanage/editpassword.html')


resetpasswordcheck = False


def resetpassword(request):
    if not request.session.get('is_login', None):
        if request.method == 'POST':
            email = request.POST.get('email')
            sameemail = models.User.objects.filter(email=email)
            if (not sameemail):
                message = "该邮箱未注册，请先注册"
                return render(request, 'usermanage/resetpassword.html',
                              context={'message': message})
            else:
                global resetpasswordcheck
                resetpasswordcheck = True
                global resetemail
                resetemail = email
                global checktext
                checktext = genrandom()
                sendcheckemail(email,str(checktext))
                return redirect('/resetpassword2/')
        return render(request, 'usermanage/resetpassword.html')
    else:
        return redirect('/editpassword/')


def resetpassword2(request):
    global resetpasswordcheck
    print(resetpasswordcheck)
    if resetpasswordcheck:
        if request.method == "POST":
            email = resetemail
            getchecktext = request.POST.get("checktext")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            getchecktext = int(getchecktext)
            if getchecktext == checktext:
                if password1 != password2:
                    message = "两次输入密码不相同，请重试!"
                    return render(request, 'usermanage/resetpassword2.html', context={'message': message})
                else:
                    if checkpassword(password2):
                        edit_userpassw = models.User.objects.get(email=email)
                        edit_userpassw.password = hash_code(password2)
                        edit_userpassw.save()
                        message = "更新密码成功，5秒后自动登出，请重新登录"
                        resetpasswordcheck = False
                        return render(request, 'usermanage/resetpassword2.html',
                                      context={'message': message, 'check': 'success'})
                    else:
                        message = "密码长度大于6"
                        return render(request, 'usermanage/resetpassword2.html', context={'message': message})
            else:
                message = "验证码不正确 即将为您跳转到上一级页面"
                return render(request, 'usermanage/resetpassword2.html', context={'message': message})
    else:

        return redirect('/resetpassword/')
    return render(request, 'usermanage/resetpassword2.html')

def dakaconfig(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    else:
        userid = request.session['user_id']
        dakaconfig = models.User.objects.get(id=userid)
        schoolid = dakaconfig.schoolid
        schoopassword = dakaconfig.schoolpassword
        moble = dakaconfig.mobile
        homemoble = dakaconfig.homemobile
        schoolgps = dakaconfig.schoolgps
        dorm = dakaconfig.dorm
        region = dakaconfig.region
        area = dakaconfig.area
        build = dakaconfig.build
        schoollon = dakaconfig.schoollon
        schoollat = dakaconfig.schoollat
        userconfig ={
            'schoolid':schoolid,
            'schoolpassword':schoopassword,
            'moble':moble,
            'homemoble':homemoble,
            'schoolgps':schoolgps,
            'dorm':dorm,
            'region':region,
            'area':area,
            'build':build,
            'schoollon':schoollon,
            'schoollat':schoollat,
        }

        regionarr = ["东风校区", "科学校区", "禹州实习训练基地", "校外走读"]
        areaarr = [
            ["一区", "二区", "三区", "丰华区", "秋实区"],
            ["宿舍区"],
            ["宿舍区"],
            ["无"]
        ]
        buildarr = [
            [
                ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼"],
                ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼", "8号楼"],
                ["附1号楼", "附2号楼", "附3号楼"],
                ["北楼", "南楼"],
                ["5号楼", "7号楼", "8号楼"]
            ],
            [
                ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼", "8号楼", "9号楼", "10号楼", "11号楼"]
            ],
            [
                ["一层：122-177", "二层：222-277", "三层：322-377", "四层：422-477", "五层：501-577", "六层：601-677"]
            ],
            [
                ["无"]
            ]
        ]
        regionstr=regionarr[int(region)]
        areastr=areaarr[int(region)][int(area)]
        buildstr=buildarr[int(region)][int(area)][int(build)]
        print(f"{regionstr}{areastr}{buildstr}")
        if request.method == "POST":
            schoolid=request.POST.get("schoolid")
            schoopassword=request.POST.get("schoolpassword")
            moble=request.POST.get("moble")
            homemoble=request.POST.get("homemoble")
            schoolgps=request.POST.get("schoolgps")
            dorm=request.POST.get("dorm")
            region=request.POST.get("region")
            area=request.POST.get("area")
            build=request.POST.get("build")
            schoollon=request.POST.get("schoollon")
            schoollat=request.POST.get("schoollat")

            dakaconfig.schoolid =  schoolid
            dakaconfig.schoolpassword = schoopassword
            dakaconfig.mobile = moble
            dakaconfig.homemobile = homemoble
            dakaconfig.schoolgps = schoolgps
            dakaconfig.dorm = dorm
            dakaconfig.region =  region
            dakaconfig.area = area
            dakaconfig.build = build
            dakaconfig.schoollon = schoollon
            dakaconfig.schoollat = schoollat
            dakaconfig.save()
            userconfig = {
                'schoolid': schoolid,
                'schoolpassword': schoopassword,
                'moble': moble,
                'homemoble': homemoble,
                'schoolgps': schoolgps,
                'dorm': dorm,
                'region': region,
                'area': area,
                'build': build,
                'schoollon': schoollon,
                'schoollat': schoollat,
            }
            message="更新资料成功，页面即将刷新"
            return render(request, 'usermanage/dakaconfig.html',{'userconfig':userconfig ,'message':message})
        return render(request, 'usermanage/dakaconfig.html',{'userconfig':userconfig})

