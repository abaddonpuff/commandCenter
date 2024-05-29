from django.urls import path, include
from centralHub import views

urlpatterns = [
    path('x/allusers', views.list_twitter, name="showalltweets"),
    path('x/xHandles/<str:twitter_handle>', views.handle_summary, name="twitter_handle_summary"),
    path('x/submit_handle/', views.submit_x_user, name='submit_handle'),
    path('',views.home_page, name='home')
]
