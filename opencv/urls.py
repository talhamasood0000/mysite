from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('livecam_feed', views.livecam_feed, name='livecam_feed'),
    path('next_page', views.next_page, name='next_page'),
]