from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import CommentModel, ContentModel, CustomUser



class UserRegiterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'blog', 'coutry', 'account_type']

        widgets = {
            'username': forms.TextInput,
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput,
        }


class ContentForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        self.user = user


    class Meta:
        model = ContentModel
        fields = '__all__'
        exclude = ('user', 'dis_like', 'like', 'viewer')

        widgets = {
            'content_title': forms.TextInput,
            'video': forms.FileInput,
            'content_albom': forms.FileInput,
        }

    def clean_video(self):
        video_file = self.cleaned_data.get('video')
        if video_file:
            if not video_file.name.endswith('.mp4'):  
                raise forms.ValidationError('Только файлы с расширением .mp4 разрешены')
        else:
            raise forms.ValidationError('Не удалось загрузить файл')
        return video_file
    


class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment']

        widgets = {
            'comment': forms.TextInput
        }


class ProfilePhotoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']


class Search(forms.Form):
    search = forms.CharField(max_length=100, label='Search....')



class ProfileComponentsChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'blog', 'coutry', 'account_type']