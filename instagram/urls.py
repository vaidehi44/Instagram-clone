
from django.urls import path, include
from . import views
from . forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

app_name = 'instagram'

urlpatterns = [
    path('signup',views.signup, name='signup'),
    path("homepage",views.HomeView.as_view(), name="homepage"),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html',authentication_form=CustomAuthForm), name='user_login'),
    path('home/', views.HomeView.as_view(),name='home'),
    path('user/post', views.addPostView.as_view(),name='addPost'),
    path('user/profile/<int:pk>', views.ShowProfileView.as_view(), name='profile'),
    path('user/profile/edit/', views.UpdateProfileView, name='editProfile'),
    path('user/profile/<int:pk>/delete', views.DeleteProfileView.as_view(), name='delete_profile'),
    path('user/post/<int:pk>', views.ShowPostView.as_view(), name='post'),
    path('user/post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),
    path('user/post/<int:pk>/edit', views.UpdatePostView.as_view(), name='edit_post'),
    path('', include('django.contrib.auth.urls'),name="logout"),
    path('user/home/like', views.LikeView, name="like"),
    path('user/home/follow', views.FollowView, name="follow"),
    path('user/home/comment/<int:pk>', views.CommentView.as_view(), name="comment"),

]

