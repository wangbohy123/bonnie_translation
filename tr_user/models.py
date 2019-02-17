from django.db import models

class Ordinary_UserManager(models.Manager):
    # 重写管理器的方法
    def get_queryset(self):
        # 修改返回的原始查询集
        return super(Ordinary_UserManager, self).get_queryset().filter(choose_translater = True)

    def create(self, accountnum, password, mail='123@qq.com'):
        # 写创建对象的方法 创建对象时可以调用该类方法
        ord = Ordinary_User()
        ord.account_number = accountnum
        ord.account_passWord = password
        ord.account_mail = mail
        ord.save()
        return ord

    def if_has(self, uname):
        try:
            self.get(account_number=uname)
        except:
            return False
        return True

class TranslaterManage(models.Manager):

    def get_queryset(self):
        return super(TranslaterManage, self).get_queryset()

    def create(self, account, password, mail='123@qq.com'):
        # 自定义管理器中创建类的方法
        tra = Translater()
        tra.account_number = account
        tra.account_passWord = password
        tra.account_mail = mail
        tra.credit_level = 4
        tra.save()
        return tra

    def if_has(self, uname):
        try:
            self.get(account_number=uname)
        except:
            return False

        return True

class Ordinary_User(models.Model):
    # 普通用户类
    account_number = models.CharField(max_length=20) # 账号
    account_passWord = models.CharField(max_length=40)# 密码
    account_mail = models.CharField(max_length=30, default='123@qq.com')#邮箱
    choose_translater = models.BooleanField(default=True) # 是否选用人工翻译
    score = models.IntegerField(default=10)  # 对结果的评分，默认满分
    users = Ordinary_UserManager()

    def __str__(self):
        return self.account_number

    class Meta:
        # 元选项 修改表的名称
        db_table = 'ordinaryUser'
        ordering = ['id'] # 指定查询的排序规则

class Translater(models.Model):
    # 翻译者类
    account_number = models.CharField(max_length=20) # 账号
    account_passWord = models.CharField(max_length=40) # 密码
    account_mail = models.CharField(max_length=30)  # 邮箱
    credit_level = models.IntegerField(null=True, default=1) # 信用等级
    score_sum = models.IntegerField(null=True, default=0) # 翻译者所得到的累计评价
    translaters = TranslaterManage() # 创建管理器对象

    def __str__(self):
        return self.account_number

    class Meta:
        db_table = 'translater'
        ordering = ['id']