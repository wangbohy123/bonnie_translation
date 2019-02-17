from django.shortcuts import render,redirect
from tr_user.models import Ordinary_User,Translater
from django.http import HttpResponse
from .models import Result,Passage

def sumbit_passage(request):
    # 提交文章进行翻译 仅限普通用户
    user_kind = request.session.get('user_kind', default=' ')
    if user_kind == 'ordinary_user':
        o_user = Ordinary_User.users.get(id=request.session.get('uid'))
    else:
        return HttpResponse("error")
    context = {
        'object':o_user, # 返回一个普通用户的对象
    }
    return render(request, 'passage.html', context)

def passage_handel(request):
    # 普通用户提交文章后的重定向
    title = request.POST['passage_title']
    text = request.POST['translation']
    o_user = Ordinary_User.users.get(id=request.session.get('uid'))
    passage = Passage.passages.create(o_user, text, title)
    return redirect('/user_center/show')

def choose_passage(request):
    # 翻译者选择文章
    passages = Passage.passages.all()
    passages_list = []
    passages_id = []
    i = {}
    for passage in passages:
        passages_list.append(passage)
        passages_id.append(passage.id)
    context = {
        'passages_list':passages_list,
        'id_list':passages_id,
    }
    return render(request, 'choose_passage.html', context)

def show_passage(request):
    # 翻译者选择文章后 将文章基本数据显示出来
    passage_id = request.GET['id']
    passage = Passage.passages.get(id=passage_id)
    translation = passage.text
    context = {
        'passage_id':passage_id,
        'translation':translation,
    }
    request.session['passage_id'] = passage_id
    # 创建一个文章的会话 记录文章的id
    return render(request, 'show_passage.html', context)

def translater_submit_passage(request):
    # 翻译者提交文章
    passage_id = request.session.get('passage_id')
    translation = request.POST['result']
    passage = Passage.passages.get(id=passage_id)

    del request.session['passage_id']

    user_id = request.session.get('uid')
    translater = Translater.translaters.get(id=user_id)

    result = Result.results.create(passage, translater, translation)
    return redirect('/user_center/show')

def show_history(request):
    # 利用用户中心反馈的get方法 接收用户牵涉到的文章
    user_kind = request.session.get('user_kind')
    if user_kind == 'ordinary_user':
        passage_id = request.GET['id']
        passage = Passage.passages.get(id=passage_id)
        result_list = passage.result_set.all()
        context = {
            'passage':passage,
            'result':result_list,
        }
        return render(request, 'show_history_o.html', context)

    elif user_kind == 'translater':
        result_id = request.GET['id']
        result = Result.results.get(id=result_id)
        passage_title = result.passage.passage_title
        translation = result.translation
        text = result.result
        context = {
            'passage_title':passage_title,
            'translation':translation,
            'text':text,
        }
        return render(request, 'show_history_t.html', context)

def handel_goal(request):
    # 处理用户对翻译结果的评分 为翻译者加分
    result_id = request.POST['id']
    goal = request.POST['goal']
    result = Result.results.get(id=result_id)
    translater = result.translater
    translater.score_sum += int(goal)
    translater.save()
    return redirect('/passage/show_history/')

def handel_result(request):
    # 处理一般用户选择的最佳结果
    result_id = request.POST['id']
    result = Result.results.get(id=result_id)
    result.if_was_chosen = True
    result.save()
    translater = result.translater
    passage = result.passage
    translater.score_sum += 100
    passage.translater = translater.id
    passage.be_translated = True
    translater.save()
    passage.save()
    return redirect('/user_center/show/')