from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from get_data.people_data import *
from viewapp.models import *
from django.http import JsonResponse
from urllib import parse
from viewapp.serializer import *
import time
from rest_framework.views import APIView
from rest_framework.response import Response


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
                return render(request, 'views.html',{'user':'true'} )
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
    page = UserWays.objects.filter(user=_user)
    return render(request, 'save_way.html', {'page': page, 'user': 'true'})


def save_scenery(request):
    _user = request.user
    if request.method == 'GET':
        arg = request.GET.get('del')
        if arg:
            d = UserScenery.objects.filter(user=_user, scenery=arg)
            d.delete()
    page = UserScenery.objects.filter(user=_user)
    return render(request, 'save_scenery.html', {'page': page, 'user': 'true'})


def user_safe(request):
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
                              {'user': arg, 'msg': '密码修改成功,请重新登入',
                               'user_name': request.user})
            else:
                return render(request, 'user_safe.html',
                              {'msg': '两次密码不一致', 'user': arg,
                               'user_name': request.user})
        else:
            return render(request, 'user_safe.html', {'msg': '旧密码有误', 'user': arg,
                                                      'user_name': request.user})
    return render(request, 'user_safe.html',
                  {'msg': '', 'user': arg, 'user_name': request.user})


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
        user_scenery.image_name = city[0].image_name
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
    way = get_way_name(is_on)
    pages = WayInfo.objects.filter(is_on=is_on)
    page = WayScenery.objects.filter(is_on=is_on)
    return render(request, 'way_info.html',
                  {"user": _arg, "pages": pages, 'page': page, "way": way.scenerys.values.tolist()[0],
                   "date": way.days.values.tolist()[0],
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
            value = [info.get('city'), date, info.get('mark'), _user, scenery, '1', '0', info.get('image_name')]
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
            if status:
                return redirect('/way_info?is_on={is_on}'.format(is_on=is_on))
            else:
                return render(request, 'make_way.html',
                              {'status': 'false', 'is_on': is_on, 'page': [], 'pages': [], 'user': user})


def map(request):
    is_on = request.GET.get('is_on')
    if is_on:
        a = get_add(is_on)
        print(a)
        if isinstance(a, dict):
            data = {
                'response': '路线可视化加载失败',
                'error': '路线景区经纬度未找到',
            }
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False},
                                content_type='application/json; charset=utf-8')
        a = a.tolist()
        b = len(a)
        return render(request, 'map.html', {'a': a, 'b': b, 'center': a[0]})


def logouts(request):
    logout(request=request)
    return render(request,'views.html',{'user':'false'})


def user_save_way(request):
    is_on =request.GET.get('is_on')
    way_list = Ways.objects.filter(is_on=is_on)
    user_way = UserWays()
    user_way.user = request.user
    user_way.is_on = is_on
    user_way.scenerys = way_list[0].scenerys
    user_way.days = way_list[0].days
    user_way.say_people = way_list[0].say_people
    user_way.start_time = way_list[0].start_time
    user_way.end_time = way_list[0].start_time[:-2]+str(int((way_list[0].start_time)[-2:])+int(way_list[0].days)-1)
    user_way.save()
    return redirect(f"/way_info/?is_on={is_on}")





class SceneryView(APIView):
    def get(self, request):
        scenery_list = SceneryAll.objects.values('city').distinct()
        serializer = ScenerySerializer(instance=scenery_list, many=True)
        return Response(serializer.data)


class ScenerysView(APIView):

    def get(self, request):
        city = request.GET.get('city')
        scenery_list = SceneryAll.objects.filter(city=city)
        serializer = ScenerysSerializer(instance=scenery_list, many=True)
        return Response(serializer.data)


class WayView(APIView):
    def get(self,request):
        is_on = request.GET.get('is_on')
        way_info_list = Ways.objects.filter(is_on=is_on)
        serializer = WaysSerialezer(instance=way_info_list,many=True)
        date = (serializer.data)[0].get('start_time')
        day = int((serializer.data[0]).get('days'))+int(date[-2:])-1
        (serializer.data[0])['end_time'] = date[:-2]+str(day)
        (serializer.data[0])['user'] = str(request.user)
        return Response(serializer.data)


class UserwayView(APIView):

    @csrf_exempt
    def post(self,request):

        serializer = UserwaySerialezer(data=request.data,many=True)
        print(serializer)
        if serializer.is_valid():
            data = UserWays.objects.create(**(serializer.data)[0])
            serializer = UserwaySerialezer(instance=data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)