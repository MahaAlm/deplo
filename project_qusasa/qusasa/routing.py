from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/echo/$', consumers.EchoConsumer.as_asgi()),
    re_path(r'ws/echo1/$', consumers.EchoGraphsConsumer.as_asgi()),
    re_path(r'ws/echo3/$', consumers.EchoModifyConsumer.as_asgi()),

]