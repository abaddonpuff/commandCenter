from django.urls import path, include
from centralHub import views

urlpatterns = [
    path('', views.list_twitter, name="showalltweets"),
    path('<str:twitter_handle>', views.handle_summary, name="twitter_handle_summary"),

]
