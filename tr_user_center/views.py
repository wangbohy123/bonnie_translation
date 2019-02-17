from django.shortcuts import render
from tr_user.models import Translater,Ordinary_User
from tr_passage.models import Passage,Result
# Create your views here.

def user_center(request):
    # 用户中心的处理
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)
    history_list = []

    if user_kind == 'ordinary_user':
        # result表示查找出来的普通用户
        user = Ordinary_User.users.get(id=uid)
        translate_history = Passage.passages.filter(ordinary_user__id=uid)
        # 过滤出普通用户提交的文章
        for objects in translate_history:
            # 将文章标题添加到列表中
            history_list.append(objects.passage_title)

        context = {
            'uname': user.account_number,
            'user_kind': user_kind,
            'result': user,
            'mail':user.account_mail,
            'history': translate_history,
        }
        return render(request, '02.html', context)

    elif user_kind == 'translater':
        user = Translater.translaters.get(id=uid)
        result_list = Result.results.filter(translater__id=uid)
        translate_history = []
        for result in result_list:
            translate_history.append(result)

        context = {
            'uname':user.account_number,
            'user_kind':user_kind,
            'result':user,
            'history':translate_history,
            'credit_level':user.credit_level,
            'goal':user.score_sum,
        }
        return render(request, '01.html', context)

def user_info(request):
    return render(request, 'main.html')

def change_pwd(request):
    return render(request, 'changePwd.html')

def user_main(request):
    return render(request, 'main.html')