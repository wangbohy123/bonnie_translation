from . import views
from django.conf.urls import url,include
app_name = 'tr_passage'
urlpatterns = [
    url(r'^submit_passage/$', views.sumbit_passage, name='submit_passage'),
    url(r'^passage_handel/$', views.passage_handel, name='passage_handel'),
    url(r'^choose_passage/$',views.choose_passage, name='choose_passage'),
    url(r'^translater_submit_passage/$', views.translater_submit_passage, name='translater_submit_passage'),
    url(r'^show_passage/$', views.show_passage, name='show_passage'),
    url(r'^show_history/$', views.show_history, name='show_history'),
    url(r'^handel_goal/$', views.handel_goal, name='handel_goal'),
    url(r'^handel_result/$', views.handel_result, name='handel_result'),
]