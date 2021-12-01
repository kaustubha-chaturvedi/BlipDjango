from django.urls import path
from Blog import views
from Blog.authviews import*
from django.contrib.auth import views as auth_views

authFunctionsList = [
    path('signup',user_signup),
    path('signin',user_login,name='signin'),
    path('signout',user_logout),
    path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}',user_activation, name='activate'),
]

urlpatterns = [
    path('',views.home),
    path('post/<str:post>',views.viewPost),
    path('tag/<str:tag>',views.tagPage),
    path('author/<str:author>',views.authorPage),
    
]+authFunctionsList
