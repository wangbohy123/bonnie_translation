
from django.conf.urls import url,include
from django.contrib import admin
from tr_user.views import index
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^user/', include('tr_user.urls',namespace='user')),
    url(r'^passage/', include('tr_passage.urls',namespace='passage')),
    url(r'^user_center/', include('tr_user_center.urls', namespace='user_center')),
]
