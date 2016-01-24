# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from views import IndexView, StartView, CatchView

__author__ = 'zengtaoxian'

urlpatterns = patterns(
    'web.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^start/$', StartView.as_view(), name='start'),
    url(r'^catch/$', CatchView.as_view(), name='catch')
)
