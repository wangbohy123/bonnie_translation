from django.db import models
from tr_user.models import Ordinary_User,Translater
# Create your models here.
class PassageManage(models.Manager):

    def create(self, ordinary_user, translation, title):
        p = Passage()
        p.ordinary_user = ordinary_user
        p.text = translation
        p.passage_title = title
        p.result = '暂无'
        p.save()
        ordinary_user.save()
        return p

class ResultManage(models.Manager):

    def create(self, passage, translater, text):
        r = Result()
        r.passage = passage
        r.translater = translater
        r.result = text
        r.translation = passage.text
        r.save()
        return r

    def choose(self, result):
        result.if_was_chosen = True
        result.save()

class Passage(models.Model):
    # 文章类
    ordinary_user = models.ForeignKey(Ordinary_User)
    translater = models.IntegerField(default=0)
    text = models.TextField(null=False, max_length=4000)
    passage_title = models.CharField(default='none', max_length=50)
    be_translated = models.BooleanField(default=False)
    passages = PassageManage()

    def __str__(self):
        return self.passage_title

    class Meta:
        db_table = 'passages'

class Result(models.Model):
    # 翻译结果类
    passage = models.ForeignKey('Passage')
    translater = models.ForeignKey(Translater)
    translation = models.TextField(max_length=4000, default=' ')
    result = models.TextField(null=False, max_length=4000)
    # 是否被选用为最合适的翻译结果
    if_was_chosen = models.BooleanField(default=False)
    results = ResultManage()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'passageResults'