# Create your views here.
from django.shortcuts import render,redirect
from sign.models import Bookinfo_a, Hearoinfo_a, save_user
from django.template import loader, RequestContext
from django.http import HttpResponse,JsonResponse

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO



# admin.html
def admin(request):
    '''登录主页'''
    # 读取COOKIE 判断是否有记录
    if 'texte' in request.COOKIES:
        texte = request.COOKIES['texte']
    else:
        texte = ''

    return render(request, 'booktest/admin.html', {'name':texte})



def index(request):
    '''首页'''
    all_booktest = Bookinfo_a.object.all()
    return render(request, 'booktest/index.html', {'all_booktest':all_booktest})




# index.html
def index_test(request):
    '''登录成功'''

    texte = request.POST.get("texte")
    passward = request.POST.get("pwd")
    chex = request.POST.get("chbox")

    # 获得验证码
    linecode = request.POST.get("vecode")
    vcode = request.session['verifycode']

    # 读取账号密码
    user = [username.user_name for username in save_user.object.all()]
    pwd = [pwd.passward for pwd in save_user.object.all()]

    if linecode != vcode:
        return redirect('/admin')

    if texte in user and passward in pwd:
        response = redirect('/index')
        if chex == "on":
            response.set_cookie("texte", texte, max_age=7*24)
        return response

    else:

        return redirect('/admin')

# /set_session
def set_session(request):
    '''设置Session'''

    request.session['username'] = 'small'
    request.session['password'] = '123'

    return HttpResponse("设置成功")



# /get_session

def get_session(request):
    '''读取Session'''

    username = request.session["username"]
    password = request.session["password"]

    return HttpResponse(username + ":" + password)


# /index_test/(\d+)
def select(request, id):
    '''读取模型类'''
    tilte = Bookinfo_a.object.get(id=id)
    ids = Hearoinfo_a.objects.filter(hbook_id=id)

    return render(request, 'booktest/select.html', {'tilte':tilte, 'ids':ids})


# /index.html 重定向

def insert(request):
    '''添加新增'''

    btitle = request.POST.get('book')
    up_date = request.POST.get('date')
    if btitle == '' or up_date == '':

        return redirect('/index')

    Bookinfo_a.object.create(btitle, up_date)

    return redirect('/index')


# /delete(\d+) 删除

def delete(request, id):
    '''删除数据'''
    tilte = Bookinfo_a.object.get(id=id)
    tilte.delete()
    return redirect('/index')


# /ve_code 读取图片
def verify_code(request):
    '''读取图片'''

    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('C:\Windows\Fonts\Verdana.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')



# /save 注册用户
def save(request):
    '''注册用户'''

    return render(request, 'booktest/save.html')


# /save_insert

def save_insert(request):
    '''注册保存数据'''

    # 1.获取用户名
    user = request.POST.get("nameuser")

    # 2.获取邮箱
    email = request.POST.get("emails")

    # 3.获取密码
    pwd = request.POST.get("pwd")
    pwdn = request.POST.get("pwdn")

    # 4.确认用户协议
    chbox = request.POST.get("chbox")

    # 判断用户名少于3个字符
    if len(user) < 3:
        return redirect("/save")

    # 判断邮箱是否为空
    if len(email) == 0:
        return redirect("/save")

    # 判断密码是否一致
    if (len(pwd) < 6 or pwd != pwdn):
        return redirect("/save")

    # 判断协议是否勾选
    if chbox == None:
        return redirect("/save")

    # 保存数据在数据库
    save_user.object.insert_user(user, email, pwd)

    return HttpResponse("注册成功")












