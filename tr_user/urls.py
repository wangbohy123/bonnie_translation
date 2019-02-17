from . import views
from django.conf.urls import url,include
app_name = 'tr_user'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$',views.index,name='index'),
    url(r'^index_for_user/$', views.index_for_user, name='index_for_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^longin_handel/$', views.login_handel, name='longin_handel'),
    url(r'^register_handel/$', views.register_handel, name='register_handel'),
    url(r'^del_session/$', views.del_session, name='del_session'),
    url(r'^verifycode$', views.verifycode, name='verifycode'),
    url(r'^baidufanyi$', views.baiduFanyi, name='baidufanyi'),
]