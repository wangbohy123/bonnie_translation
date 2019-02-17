from . import views
from django.conf.urls import url,include
app_name = 'tr_user_center'
urlpatterns = [
    url(r'^show/$', views.user_center, name='show'),
    url(r'^user_info/$',views.user_info, name='user_info' ),
    url(r'^change_pwd/$', views.change_pwd, name='change_pwd'),
    url(r'^user_main/$', views.user_center, name='user_main'),
]