from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import (authenticate,
                                  login,
                                    logout,
                                      update_session_auth_hash
                                      )


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (CommentModel,
                      ContentModel,
                        CustomUser)


from .forms import (UserRegiterForm,
                     ContentForm,
                       CommentForm,
                         ProfilePhotoForm,
                           Search,
                             ProfileComponentsChange
                             )

from django.views.generic import TemplateView,  DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest
import os



class ProfilePhotoView(TemplateView):
    template_name = 'uplouds/profile_photo.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):

        form = ProfilePhotoForm()

        return render(request, self.template_name, {'form':form})
    
    def post(self, request):

        user_profile_photo, created = CustomUser.objects.get_or_create(username=request.user)

        if  not created and user_profile_photo.profile_photo:
            messages.success(request, '')

        form = ProfilePhotoForm(request.POST, request.FILES, instance=user_profile_photo)
        if form.is_valid():
            new_photo_ = form.save(commit=False)
            new_photo_.user = request.user
            new_photo_.save()
            return redirect('home')
            
        return render(request, self.template_name, {'form':form})
            
            

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contents'] = ContentModel.objects.all()
        return context



class UserRegisterView(TemplateView):
    template_name = 'authofivation/register.html'

    
    def get(self, request):
        form = UserRegiterForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form = UserRegiterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        return render(request, self.template_name, {'form':form})
    

class LoginView(TemplateView):
    template_name = 'authofivation/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        return render(request, self.template_name)
    



class ContentUploudView(TemplateView):
    template_name = 'uplouds/content_uploud.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        
        form = ContentForm()
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request, *args, **kwargs):
        
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            new_ = form.save(commit=False)
            new_.user = request.user
            new_.save()
            return redirect('home')
        
        return render(request, self.template_name, {'form':form})
    


class LikeButton(View):

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self,request, pk:int, *args, **kwargs):

        like_model = ContentModel.objects.get(id=pk)

        if request.user not in like_model.like.all():
            like_model.like.add(request.user)
        
        else:
            like_model.like.remove(request.user)

            like_model.save()

        return  JsonResponse({'messgae': 'Like Send Is Succses'})



class CommentView(DetailView):
    template_name = 'uplouds/comment.html'
    model = ContentModel

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
        try:
            commentarion_obj = self.get_object()
        except ContentModel.DoesNotExist:
            return None

        comments = CommentModel.objects.filter(content=commentarion_obj)
        form = CommentForm()

        return render(request, 'uplouds/comment_uploud.html', {'form': form, 'comments': comments, 'commentarion_obj': commentarion_obj})

    def post(self, request, *args, **kwargs):
        
        comment_obj  = self.get_object()
        commets = CommentModel.objects.filter(content = comment_obj)

        form = CommentForm(request.POST)
        if form.is_valid():
            
            new_cooment_ = form.save(commit=False)
            new_cooment_.user = request.user
            new_cooment_.content = comment_obj
            new_cooment_.save()

            return JsonResponse({'message': 'Comment Uploud Succses'})




class ContentDetailView(DetailView):
    template_name = 'detail_pages/content_detail.html'
    model = ContentModel
    context_object_name = 'contents'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user

        post_id = obj.id

        viewed_posts = self.request.session.get('viewed_posts', [])

        if post_id not in viewed_posts:
            obj.viewer += 1
            obj.save()

            viewed_posts.append(post_id)
            self.request.session['viewed_posts'] = viewed_posts

        return obj



class UserProfileView(TemplateView):
    template_name = 'pages/user_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, **kwargs)
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['contents'] = ContentModel.objects.filter(user=user)
        return context
    


class ContentDeleteView(View):

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    

    def get(self, request, pk:int, *args, **kwargs):

        content = get_object_or_404(ContentModel, pk=pk)

        if request.user == content.user:

            file_path = os.path.join(settings.MEDIA_ROOT, str(content.video))
            os.remove(file_path)
            content.delete()  # Удаляем сам объект ContentModel


            return JsonResponse({'message': 'Content Deleted Successfully'})



class SearchContent(TemplateView):
    template_name= 'pages/search.html'


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        form = Search(request.GET or None)
        content = None

        if form.is_valid():
            search = form.cleaned_data['search']
            content = ContentModel.objects.filter(content_title__icontains = search)


        return render(request, self.template_name, {'form':form, 'contens':content})



class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    template_name = 'uplouds/profile_update.html'
    form_class = ProfileComponentsChange
    model = CustomUser
    success_url = reverse_lazy('user_profile')


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset = None):
        return self.request.user
    


class PasswordChangeView(TemplateView):
    template_name = 'uplouds/password_change.html'
    form_class = PasswordChangeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name,  {'form':form})
    
    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password Changed')
            return redirect('user_profile')
        
        return render(request, self.template_name, {'form':form})




class SubscribeToUserView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    

    def get(self, request, pk:int):

        subscribe_model = CustomUser.objects.get(pk=pk)

        if request.user not in subscribe_model.subscribe.all():
            subscribe_model.subscribe.add(request.user)

        else:
            subscribe_model.subscribe.remove(request.user)
            subscribe_model.save()
            return JsonResponse({'message':'Вы Успешно Отписались '})
        
        return JsonResponse({'message':'Вы Успешно Подписались '})

        

class LogoutView(View):


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        return redirect('login')




class UpdateContent(UpdateView):
    model = ContentModel
    form_class = ContentForm
    template_name = 'uplouds/change_content.html'
    success_url = reverse_lazy('user_profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return redirect('home') 
        context['form'] = ContentForm(user=user, instance=self.object)
        return context


class ProfileDetailView(DetailView):
    model = CustomUser
    context_object_name = 'profile'
    template_name = 'pages/profile.html'


@login_required
def get_trend_videos(request):

    get_trend_videos = ContentModel.objects.filter(viewer__gt = 10000)

    return render(request, 'pages/get_trned_content.html', {'trend':get_trend_videos})



@login_required
def get_user_category_contents(request):
    user = request.user

    mens = ContentModel.objects.filter(content_type = user.account_type)

    return render(request, 'pages/ineresing.html', {'interes':mens})


from django.conf import settings

@login_required
def dislike(request: HttpRequest, pk) -> HttpRequest:
    dislike_model = ContentModel.objects.get(pk=pk)

    if request.user not in dislike_model.dis_like.all():
        dislike_model.dis_like.add(request.user)
        if dislike_model.dis_like.count() > 1:
            # Получаем путь к файлу и удаляем его
            file_path = os.path.join(settings.MEDIA_ROOT, str(dislike_model.video))
            os.remove(file_path)
            dislike_model.delete()  # Удаляем сам объект ContentModel
    else:
        dislike_model.dis_like.remove(request.user)
    
    return JsonResponse({'message': 'Ваши действия были успешно сохранены'})



class GetUserFollowers(TemplateView):
    template_name = 'detail_pages/followers.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk:int, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        context = user
        user_followers = user.subscribe.all()
        return render(request, self.template_name, {'user_followers':user_followers})
        
    

@login_required
def get_content_likes(request: HttpRequest, pk) -> HttpRequest:
    
    user = ContentModel.objects.get(pk=pk)
    context = user
    content_likes = user.like.all()
    return render(request, 'detail_pages/user_likes.html', {'content_likes':content_likes})


class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,)
    

@login_required
def commentarion_delete_view(request : HttpRequest, pk) -> HttpRequest:

    comment = get_object_or_404(CommentModel, pk=pk)

    if request.user == comment.user:
        comment.delete()

    return JsonResponse({'message': 'Comment Delete Succses'})


class GetUserCommentarion(TemplateView):
    template_name = 'pages/comments.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        comments = super().get_context_data(**kwargs)
        user = self.request.user
        comments['commentarions'] = CommentModel.objects.filter(user=user)
        return comments
    


