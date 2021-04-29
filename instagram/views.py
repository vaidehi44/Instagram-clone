from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import  UserForm, ProfileForm, UserEditForm, ProfileEditForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import Posts, Profile, Like, Follow, Comments
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django import forms


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile.fullname = profile_form.cleaned_data.get('fullname')
            user.save()
            return HttpResponseRedirect(reverse('instagram:signup'))
            
        else:
            return render(request, 'signup.html', {'user_form':user_form, 'profile_form':profile_form,"invalid": True} )

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request,'signup.html',{'user_form':user_form, 'profile_form':profile_form})


class HomeView(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'home.html' 
    queryset = Posts.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView , self).get_context_data(**kwargs)
        context['profile_sugg'] = Profile.objects.all()
        context['comment_form'] = CommentForm
        context['title'] = 'Home'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    

class addPostView(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'addPost.html'
    fields = ('title','description','image')
    success_url = reverse_lazy('instagram:homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


class ShowPostView(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'Post.html'
    fields = '__all__'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ShowPostView , self).get_context_data(**kwargs)
        context['title'] = Posts.objects.get(id=self.kwargs['pk']).title
        return context

    
    
class ShowProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'Profile.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ShowProfileView , self).get_context_data(**kwargs)
        context['title'] = 'Profile'
        context['all_posts'] = Posts.objects.filter(user=self.request.user)
        context['followers'] = Follow.objects.filter(profile=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteProfileView(DeleteView):
    model = User
    template_name="Profile.html"
    success_url = reverse_lazy("instagram:signup")


class DeletePostView(DeleteView):
    model = Posts
    template_name="Post.html"

    def get_success_url(self):
           user_pk = self.request.user.id
           profile_pk = User.objects.get(id=user_pk).profile.pk
           return reverse("instagram:profile", kwargs={"pk": profile_pk})


class UpdatePostView(UpdateView):
    model = Posts
    template_name="edit_post.html"
    fields = ("title","description","image")

    def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("instagram:post", kwargs={"pk": pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].widget = forms.FileInput()
        return form

  
@login_required
def UpdateProfileView(request):
    user = request.user
    user_form = UserEditForm(request.POST or None, 
                        initial={'username': user.username, 
                                 'email': user.email}, instance = user)
    user_profile_form = ProfileEditForm( request.POST or None, request.FILES or None,
                        initial = {'bio': user.profile.bio,
                        'fullname': user.profile.fullname }, instance = user.profile)

    if request.method == 'POST':
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return HttpResponseRedirect(reverse('instagram:profile', args=[request.user.profile.id] ))
    context = {
        "user_form": user_form,
        "user_profile_form": user_profile_form
    }
    return render(request, "edit_profile.html", context)


@login_required
def LikeView(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Posts.objects.get(id=post_id)
        #profile = Profile.objects.get(user=user)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post=post_obj)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

    return redirect('instagram:home')


@login_required
def FollowView(request):
    user = request.user#user who wants to follow
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        #follow_user = User.objects.get(id=Profile.objects.get(pk=profile_id).user.id)#user to be followed
        follow_profile = Profile.objects.get(id=profile_id)

        if user in follow_profile.followers.all():
            follow_profile.followers.remove(user)
        else:
            follow_profile.followers.add(user)

        follow_status, created = Follow.objects.get_or_create(user=user, profile=follow_profile)

        if not created:
            if follow_status.value=='Follow':
                follow_status.value='Following'
            else:
                follow_status.value='Follow'
        else:
            follow_status.value='Follow'

            follow_profile.save()
            follow_status.save()
            
    return redirect('instagram:home')


class CommentView(CreateView,LoginRequiredMixin):
    model = Comments
    form_class = CommentForm
    template_name = 'home.html'
    success_url = reverse_lazy('instagram:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)





