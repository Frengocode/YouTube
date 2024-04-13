from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_countries.fields import CountryField

class AccountType(models.TextChoices):
    FOR_KID = 'Для Младшего Ребёнка ', 'Для Младшего Ребёнка'
    FOR_ME = 'Для Себя', 'Для Себя'
    FOR_ANY_PEOPLE = 'Для Семьи', 'Для Семьи'
    FOR_ALL = 'Для Всех', 'Для Всех'



# class ContentType(models.TextChoices):

#     FOR_OLDS = 'Для Взрослых', 'Для Взрослых'
#     FOR_KIDS = 'Для Детей', 'Для Детей'
#     FOR_STDUDENTS = 'Для Подростков', 'Для Подростков'
#     FOR_ALL = 'Для Всех', 'Для Всех'



class BlogType(models.TextChoices):

    PUBLIG_BLOG = 'Личный Блог', 'Личный Блог'
    BECOME_A_STAR_BLOGER = 'Профессиональный Блог', 'Профессиональный Блог'




class ContentModel(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    content_title = models.CharField(max_length=60)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'btn_like')
    content_albom = models.ImageField(upload_to='content_albom/')
    video = models.FileField(upload_to='videos/')
    content_type = models.CharField(max_length=50,choices=AccountType)
    created_at  = models.DateTimeField(auto_now_add=True)
    dis_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dont_like')
    viewer = models.PositiveIntegerField(default=0)



    class Meta:
        ordering = ['-created_at']



class  CustomUser(AbstractUser):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='user_profile_photo/')
    subscribe = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='follow_to_user')
    coutry = CountryField()
    blog = models.CharField(max_length=80, choices=BlogType)
    account_type = models.CharField(max_length=50, verbose_name='выберите для кого вы создаёте этот аккаунт ' , choices=AccountType)


class CommentModel(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=50)
    like = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='love_button', null=True)
    created_at  = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-created_at']
