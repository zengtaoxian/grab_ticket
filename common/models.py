# -*- coding: utf-8 -*-
__author__ = 'zengtaoxian'

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?\d{11}$', message='电话号码格式错误, 11位')


class AccountManger(BaseUserManager):
    def create_user(self, username, password):
        account = self.model(username=username, is_staff=False,
                             is_superuser=False)

        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, password):
        account = self.create_user(username, password)

        account.is_staff = True
        account.is_active = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    username = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    telephone = models.CharField(max_length=16, default='', null=True, blank=True, verbose_name='手机号码',
                                 validators=[phone_regex])
    email = models.EmailField(default='', null=True, blank=True, verbose_name='邮箱')
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES, verbose_name='性别')

    register_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    login_time = models.DateTimeField(auto_now=True, verbose_name='登录时间')
    is_staff = models.BooleanField(default=False, verbose_name='管理员标识')

    object = AccountManger()
    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = u'账户'
        verbose_name_plural = '账户列表'
        ordering = ['username']


class Passenger(models.Model):
    USER_TYPE_CHOICES = (
        ('C', '普通'),
        ('Ｓ', '学生'),
    )
    user_name = models.CharField(max_length=128, verbose_name='用户名')
    user_id = models.CharField(max_length=18, verbose_name='身份证')
    user_type = models.CharField(max_length=1, default='C', choices=USER_TYPE_CHOICES, verbose_name='用户类型')

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name = '乘客'
        verbose_name_plural = '乘客列表'
        ordering = ['user_name']


class Train(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '车次'
        verbose_name_plural = '车次列表'
        ordering = ['name']


class Seat(models.Model):
    SEAT_TYPE_CHOICES = (
        ('QB', '全部'),
        ('SWZ', '商务座'),
        ('TDZ', '特等座'),
        ('YDZ', '一等座'),
        ('EDZ', '二等座'),
        ('GJRW', '高级软卧'),
        ('RW', '软卧'),
        ('YW', '硬卧'),
        ('DW', '动卧'),
        ('GJDW', '高级动卧'),
        ('RZ', '软座'),
        ('YZ', '硬座'),
        ('WZ', '无座')
    )
    seat_type = models.CharField(max_length=5, default='QB', verbose_name='席座类型')

    def __unicode__(self):
        return self.seat_type

    class Meta:
        verbose_name = '席座'
        verbose_name_plural = '席座列表'
        ordering = ['seat_type']


class BackupDate(models.Model):
    date = models.DateField(verbose_name='日期')

    def __unicode__(self):
        return self.date

    class Meta:
        verbose_name = '备选日期'
        verbose_name_plural = '备选日期列表'
        ordering = ['date']


class Ticket(models.Model):
    TRIP_TYPE_CHOICES = (
        ('S', '单程'),
        ('R', '往返')
    )

    TRAIN_TYPE_CHOICES = (
        ('A', '全部'),
        ('G', '高铁'),
        ('D', '动车'),
        ('Z', '直达'),
        ('T', '快车'),
        ('O', '其他')
    )

    FIRST_CHOICES = (
        ('T', '优先车次'),
        ('S', '优先席位')
    )

    trip_type = models.CharField(max_length=1, default='S', choices=TRIP_TYPE_CHOICES, verbose_name='行程类型')
    from_address = models.CharField(max_length=32, blank=True, null=True, verbose_name='出发地')
    to_address = models.CharField(max_length=32, blank=True, null=True, verbose_name='目的地')
    left_date = models.DateField(default=timezone.now(), blank=True, null=True, verbose_name='出发日')
    back_date = models.DateField(default=timezone.now(), blank=True, null=True, verbose_name='返程日')
    train_type = models.CharField(max_length=1, default='A', choices=TRAIN_TYPE_CHOICES, verbose_name='车次类型')
    start_time = models.CharField(max_length=32, default='00002400', verbose_name='发车时间')
    passenger = models.ForeignKey(Passenger, blank=True, null=True, verbose_name='乘车人')
    train_first = models.ForeignKey(Train, blank=True, null=True, verbose_name='优先车次')
    seat_first = models.ForeignKey(Seat, blank=True, null=True, verbose_name='优先席位')
    backup_date = models.ForeignKey(BackupDate, blank=True, null=True, verbose_name='备选日期')
    first_set = models.CharField(max_length=1, default='S', choices=FIRST_CHOICES, verbose_name='优先设置')

    def __unicode__(self):
        return self.from_address + self.to_address

    class Meta:
        verbose_name = '车票'
        verbose_name_plural = '车票列表'
        ordering = ['train_type']


class IDCode(models.Model):
    code = models.CharField(max_length=36, unique=True, verbose_name='编码')
    result = models.IntegerField(verbose_name='结果', default=0)
    index = models.IntegerField(verbose_name='索引', default=1)

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = '验证码列表'
        ordering = ['code']