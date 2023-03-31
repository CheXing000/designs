from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from get_data.people_data import *
from viewapp.models import *
from urllib import parse
import time


def page_new(request):
    if request.user.is_authenticated:
        user = 'true'
    else:
        user = 'false'
    url = request.get_full_path()
    arg = url.split('=')[-1]
    arg = parse.unquote(arg)
    print(arg)
    if 'new_page' in arg or arg.isdigit():
        arg = '中国'
        scenery_list = SceneryAll.objects.all()
    else:
        scenery_list = SceneryAll.objects.filter(city=arg)
    if not scenery_list:
        scenery_list = SceneryAll.objects.filter(scenery=arg)
        print(scenery_list)
    return render(request, 'new_page.html', {'page': scenery_list, 'user': user, 'the_value': arg})


def views_page(request):
    org = 'false'
    if request.user.is_authenticated:
        org = 'true'
    return render(request, 'views.html', {'user': org})


def login_page(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get("user")
        password = request.POST.get("pwd")
        if username == '' or password == '':
            return render(request, 'login.html', {"error_msg": "用户名或密码不能为空"})
        else:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'views.html', )
            else:
                return render(request, 'login.html', {"error_msg": "用户或密码错误"})


def index_page(request):
    if request.user.is_authenticated:
        arg = 'true'
    else:
        arg = 'false'
    if request.method == "GET":
        return render(request, 'index.html', {'status': arg})
    username = request.POST.get("user", '')
    pwd = request.POST.get("pwd", "")
    email = request.POST.get("email", "")
    try:
        user = User.objects.create_user(username=username, password=pwd, email=email)
        user.save()
        return redirect('/login', )
    except:
        return render(request, 'index.html', {"error_msg": "注册失败", 'status': arg})


def people_page(request):
    _arg = 'false'
    if request.user.is_authenticated:
        _arg = 'true'
    if request.method == 'POST':
        _user = UserInfo()
        _user.user = request.user
        _user.name = request.POST.get('name')
        _user.sex = request.POST.get('sex')
        _user.phone = request.POST.get('phone')
        _user.email = request.POST.get('email')
        _user.myself = request.POST.get('self')
        _user.good_at = request.POST.get('happy')
        _user.go_way = request.POST.get('go_way')
        _user.save()
        time.sleep(1)
        arg = UserInfo.objects.filter(user=request.user)
        return render(request, 'people.html', {'name': arg[0].name,
                                               'sex': arg[0].sex,
                                               'phone': arg[0].phone,
                                               'email': arg[0].email,
                                               'myself': arg[0].myself,
                                               'good-at': arg[0].good_at,
                                               'go_way': arg[0].go_way,
                                               'user': _arg})
    return render(request, 'peolple_page.html', {'user': _arg})


def people(request):
    _arg = 'false'
    if request.user.is_authenticated:
        _arg = 'true'
    arg = UserInfo.objects.filter(user=request.user)
    if arg:
        return render(request, 'people.html', {'name': arg[0].name,
                                               'sex': arg[0].sex,
                                               'phone': arg[0].phone,
                                               'email': arg[0].email,
                                               'myself': arg[0].myself,
                                               'good-at': arg[0].good_at,
                                               'go_way': arg[0].go_way,
                                               'user': _arg})
    else:
        return render(request, 'people.html', {'name': '请完善信息',
                                               'sex': '请完善信息',
                                               'phone': '请完善信息',
                                               'email': '请完善信息',
                                               'myself': '请完善信息',
                                               'good_at': '请完善信息',
                                               'go_way': '请完善信息',
                                               'user': _arg})


def save_ways(request):
    _user = request.user
    if request.method == 'GET':
        arg = request.GET.get('del')
        if arg:
            d = UserWays.objects.filter(user=_user, is_on=arg)
            d.delete()
    page = UserWays.objects.all()
    print(page)
    return render(request, 'save_way.html', {'page': page, 'user': 'true'})


def save_scenery(request):
    _user = request.user
    if request.method == 'GET':
        arg = request.GET.get('del')
        print(arg)
        if arg:
            d = UserScenery.objects.filter(user=_user, scenery=arg)
            d.delete()
    page = UserScenery.objects.all()
    return render(request, 'save_scenery.html', {'page': page, 'user': 'true'})


def user_safe(request):
    print(request.user)
    user_safe = UserSafe.objects.filter(user_name=request.user)
    if request.user.is_authenticated:
        arg = 'true'
    else:
        arg = 'false'
    if request.method == 'POST':
        old_pwd = request.POST.get('old_password')
        new_pwd = request.POST.get('new_password')
        new_pwd_1 = request.POST.get('new_password_1')
        user = User.objects.get(username=request.user)
        if user.check_password(old_pwd):
            if new_pwd == new_pwd_1:
                user.set_password(new_pwd)
                user.save()
                arg = 'false'
                return render(request, 'user_safe.html',
                              {'user': arg, 'msg': '密码修改成功,请重新登入', 'user_id': user_safe[0].user_id,
                               'user_name': user_safe[0].user_name})
            else:
                return render(request, 'user_safe.html',
                              {'msg': '两次密码不一致', 'user': arg, 'user_id': user_safe[0].user_id,
                               'user_name': user_safe[0].user_name})
        else:
            return render(request, 'user_safe.html', {'msg': '旧密码有误', 'user': arg, 'user_id': user_safe[0].user_id,
                                                      'user_name': user_safe[0].user_name})
    return render(request, 'user_safe.html',
                  {'msg': '', 'user': arg, 'user_id': user_safe[0].user_id, 'user_name': user_safe[0].user_name})


def scenery_page(request):
    arg = request.GET.get('scenery')
    is_save = request.GET.get('is_save')
    scenery_list = ScenerySee.objects.filter(scenery_name=arg)
    if is_save and not UserScenery.objects.filter(scenery=arg).exists():
        city = SceneryAll.objects.filter(scenery=arg)
        user_scenery = UserScenery()
        user_scenery.city = city[0].city
        user_scenery.user = request.user
        user_scenery.scenery = arg
        user_scenery.mark = scenery_list[0].mark
        user_scenery.rank = scenery_list[0].rank
        user_scenery.save()
    if request.user.is_authenticated:
        user = 'true'
    else:
        user = 'false'
    return render(request, 'scenery.html', context={'scenery_detail': scenery_list[0].scenery_detail,
                                                    'scenery_way': scenery_list[0].scenery_way,
                                                    'scenery_address': scenery_list[0].scenery_address,
                                                    'scenery_open': scenery_list[0].scenery_open,
                                                    'scenery_mark': scenery_list[0].mark,
                                                    'scenery_rank': scenery_list[0].rank,
                                                    'scenery_other': scenery_list[0].scenery_other,
                                                    'scenery_menpiao': scenery_list[0].scenery_menpiao,
                                                    'scenery_name': scenery_list[0].scenery_name,
                                                    'user': user})


def photo_page(request):
    url = request.get_full_path()
    arg = url.split('=')[-1]
    arg = parse.unquote(arg)
    city = SceneryAll.objects.filter(scenery=arg)
    path = "/static/image/city_image/" + city[0].city + '/' + arg + '/'
    return render(request, 'photo.html', {'image_path': path, 'scenery_name': arg})


def hot_page(request):
    if request.user.is_authenticated:
        user = 'true'
    else:
        user = 'false'
    arg = get_hot_city()
    arg.update({'user': user})
    return render(request, 'hot_page.html', arg)


def option_page(request):
    global o_arg
    scenery = request.GET.get('scenery')
    print(scenery)
    if request.user.is_authenticated:
        _arg = 'true'
        if request.method == 'POST':
            option = request.POST.get('option')
            if OptionScenery.objects.filter(options=option, user=request.user).exists():
                pass
            else:
                _option = OptionScenery()
                _option.user = request.user
                _option.user_id = '111'
                _option.options = option
                _option.scenery = scenery
                _option.options_time = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
                _option.save()
            option_info = OptionScenery.objects.all().order_by('-create_time')
            return render(request, 'option_page.html', {'page': option_info, 'arg': _arg, 'scenery': scenery})
        else:
            arg = request.GET.get('del')
            o_arg = 'true'
            if arg:
                a = OptionScenery.objects.filter(options_time=arg, user=request.user, scenery=scenery).delete()
                if a[0] == 0:
                    o_arg = 'false'
            option_info = OptionScenery.objects.filter(scenery=scenery).order_by('-create_time')
            return render(request, 'option_page.html',
                          {'page': option_info, 'arg': _arg, 'o_arg': o_arg, 'scenery': scenery})
    else:
        _arg = 'false'
        o_arg = 'false'
    option_info = OptionScenery.objects.filter(scenery=scenery).order_by('-create_time')
    return render(request, 'option_page.html', {'page': option_info, 'arg': _arg, 'o_arg': o_arg, 'scenery': scenery})


def hot_way(request):
    if request.user.is_authenticated:
        user = 'true'
    else:
        user = 'false'
    page = Ways.objects.all()
    return render(request, 'hot_way.html', {'page': page, 'user': user})


def way_info(request):
    if request.user.is_authenticated:
        _arg = 'true'
    else:
        _arg = 'false'
    url = request.get_full_path()
    is_on = url.split('=')[-1]
    is_on = parse.unquote(is_on)
    if is_on in ('/way_info/', ''):
        page = Ways.objects.all()
        return render(request, 'hot_way.html', {'page': page})
    way = Ways.objects.filter(is_on=is_on)
    pages = WayInfo.objects.filter(is_on=is_on)
    page = WayScenery.objects.filter(is_on=is_on)
    print(way)
    return render(request, 'way_info.html',
                  {"user": _arg, "pages": pages, 'page': page, "way": way[0].scenerys, "date": way[0].days,
                   "is_on": is_on})


def way_option(request):
    global o_arg
    is_on = request.GET.get('is_on')
    if request.user.is_authenticated:

        _arg = 'true'
        if request.method == 'POST':
            option = request.POST.get('option')
            if OptionWay.objects.filter(options=option, user=request.user).exists():
                pass
            else:
                _option = OptionWay()
                _option.user = request.user
                _option.user_id = '111'
                _option.options = option
                _option.is_on = is_on
                _option.option_time = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
                _option.save()
            option_info = OptionWay.objects.filter(is_on=is_on).order_by('-create_time')
            return render(request, 'way_option.html',
                          {'page': option_info, 'arg': _arg, 'o_arg': 'true', 'is_on': is_on})
        else:
            arg = request.GET.get('del')
            o_arg = 'true'
            if arg:
                a = OptionWay.objects.filter(option_time=arg, user=request.user, is_on=is_on).delete()
                if a[0] == 1:
                    o_arg = 'true'
                else:
                    o_arg = 'false'
            option_info = OptionWay.objects.filter(is_on=is_on).order_by('-create_time')
            return render(request, 'way_option.html',
                          {'page': option_info, 'arg': _arg, 'o_arg': o_arg, 'is_on': is_on})
    else:
        _arg = 'false'
        o_arg = 'false'
    option_info = OptionWay.objects.filter(is_on=is_on).order_by('-create_time')
    return render(request, 'way_option.html', {'page': option_info, 'arg': _arg, 'o_arg': o_arg, 'is_on': is_on})


def make_way(request):
    if request.user.is_authenticated:
        user = 'true'
    else:
        user = 'false'
    _user = request.user
    if request.method == 'POST' and user == 'true':
        scenery = request.POST.get('scenery')
        date = request.POST.get('date')
        info = get_scenery_info(scenery)
        if not UserWay.objects.filter(user=_user, is_web='0', scenery=scenery, date=date).exists() and info:
            value = [info.get('city'), date, info.get('mark'), _user, scenery, '1', '0']
            save_way(value)
        time.sleep(1)
        page = UserWay.objects.filter(user=_user, is_web='0').order_by('date')
        df = pd.DataFrame(list(page.values()))
        if df.empty:
            pages = []
        else:
            pages = get_date(df[['city', 'date']])
        return render(request, 'make_way.html', {'page': page, 'user': user, 'pages': pages})
    elif request.method == 'POST' and user == 'false':
        return render(request, 'login.html')
    elif request.method == 'GET':
        del_arg = request.GET.get('del')
        if del_arg:
            del_list = del_arg.split('=')
            d = UserWay.objects.filter(user=_user, is_web='0', scenery=del_list[0], date=del_list[1])
            d.delete()
            page = UserWay.objects.filter(user=_user, is_web='0').order_by('date')
            df = pd.DataFrame(list(page.values()))
            if df.empty:
                pages = []
            else:
                pages = get_date(df[['city', 'date']])
            return render(request, 'make_way.html', {'page': page, 'user': user, 'pages': pages})
        else:
            page = UserWay.objects.filter(user=_user, is_web='0').order_by('create_time')
            df = pd.DataFrame(list(page.values()))
            status, is_on = update_way_status(_user, df)
            print(status)
            if status:
                way = Ways.objects.filter(is_on=is_on)
                _pages = WayInfo.objects.filter(is_on=is_on)
                _page = WayScenery.objects.filter(is_on=is_on)

                return render(request, 'way_info.html',
                              {"pages": _pages, 'page': _page, "way": 'bbbb', "date": 'aaa'})
            else:
                return render(request, 'make_way.html',
                              {'status': 'false', 'is_on': is_on, 'page': [], 'pages': [], 'user': user})


def map(request):
    is_on= request.GET.get('is_on')
    if is_on:
        a = get_add(is_on)
        a = a.tolist()
        b = len(a)
        return render(request, 'map.html',{'a':a,'b':b,'center':a[0]})
