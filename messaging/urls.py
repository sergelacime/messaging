from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'$', views.login_view),
    re_path(r'login/$', views.login_view, name='login'),
    re_path(r'logout/$', views.logout_view, name='logout'),
    re_path(r'inbox/$', views.inbox_view, name='inbox'),
    re_path('chat_view/', views.chat_view, name='chat_view'),
    # re_path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    re_path(r'^(?P<id>[0-9]+)/delete/',views.delete_message,name="delete_message"),
    re_path('compose/', views.compose_message, name='compose'),
    # re_path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    re_path(r'^(?P<id>[0-9]+)/edit/',views.edit_message,name="edit_message"),

]
