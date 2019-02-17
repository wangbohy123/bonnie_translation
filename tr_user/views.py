from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.db.models import Max
from django.http import *
from .models import *

def register(request):
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image':image,
    }
    return render(request, 'register.html')

def login(request):
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image':image,
    }
    return render(request, 'login.html', context)

def login_handel(request):
    # 登录会话
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    user_kind= post.get('user_kind')
    code = post.get('verifycode')
    verifycode = request.session['verifycode']
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    # if code != verifycode:
    #     return HttpResponse('验证码错误')
    if user_kind == 'ordinary_user':
        user = Ordinary_User.users.filter(account_number=uname)
        if len(user) == 1:
            try:
                temp = Ordinary_User.users.get(account_number=uname, account_passWord=pwd)
                print(temp.account_number)
                id = temp.id
            except:
                return HttpResponse('密码错误')
        else:
            return redirect('/user/login/')

    elif user_kind == 'translater':
        user = Translater.translaters.filter(account_number=uname)
        if len(user) == 1:
            try:
                temp = Translater.translaters.get(account_number=uname, account_passWord=pwd)
                print(temp.account_number)
                id = temp.id
            except:
                return HttpResponse('密码错误')
        else:
            return redirect('/user/login/')

    else:
        return HttpResponse('请输入用户种类')

    request.session['uid'] = id
    request.session['user_kind'] = user_kind
    return redirect('/user/index_for_user/')

def register_handel(request):
    # 注册
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    cpwd = post.get('cpwd')
    mail = post.get('email', default='123@qq.com')
    user_kind = post.get('user_kind')
    if upwd != cpwd:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    if user_kind == 'ordinary_user':
        if Ordinary_User.users.if_has(uname):
            return HttpResponse('repeated')
        o_user = Ordinary_User.users.create(uname, pwd, mail)

    elif user_kind == 'translater':
        if Translater.translaters.if_has(uname):
            return HttpResponse('repeated')
        t_user = Translater.translaters.create(uname, pwd, mail)

    return redirect('/user/login/')

def del_session(request):
    # 清除会话的功能
    request.session.flush()
    return redirect('/user/index/')

def index(request):
    if request.session.get('uid', default='') == '':
        context = {'fanyi_content':'请输入翻译的文本'}
        if request.method == 'POST':
            post = request.POST
            fanyi_content = post.get('fanyi_content')
            print('fanyi_content:{x}'.format(x=fanyi_content))
            result = baiduFanyi(fanyi_content)
            context['fanyi_content'] = fanyi_content
            context['result'] = result
        return render(request, 'index.html', context)
    else:
        return redirect('/user/index_for_user/')

def index_for_user(request):

    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    context = {
        'uname':user.account_number,
        'fanyi_content': '请输入翻译的文本',
    }
    if request.method == 'POST':
        post = request.POST
        fanyi_content = post.get('fanyi_content')
        result = baiduFanyi(fanyi_content)
        context = {
            'uname': user.account_number,
            'fanyi_content': fanyi_content,
            'result': result,
        }
    return render(request, 'index_for_user.html',context)


def baiduFanyi(request):
    import http
    import hashlib
    import urllib.request
    import random
    import json
    q = request
    print('q:{x}'.format(x=q))
    if len(q.split()) == 0 or q == '请输入翻译的文本':
        return '不能为空'
    appid = '20171205000102472'
    secretKey = 'WRBWX979zs9ON1vksp1R'
    myurl = '/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = sign.encode('UTF-8')
    m1 = hashlib.md5()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
    # response是HTTPResponse对象
    response = httpClient.getresponse()
    html = response.read().decode('UTF-8')
    target2 = json.loads(html)
    print('target2:{x}'.format(x=target2))
    src = target2['trans_result'][0]['dst']
    outStr = src
    return outStr

def verifycode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype("Dengb.ttf", 16)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    from io import StringIO,BytesIO
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')