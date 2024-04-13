from django.urls import path
from .views import (HomePageView,
                    UpdateUserProfile,
                       ProfilePhotoView,
                         UserProfileView,
                           UserRegisterView,
                             LoginView,
                                 SearchContent,
                                   CommentView,
                                     LikeButton,
                                       SubscribeToUserView,
                                        ContentDeleteView,
                                          ContentDetailView,
                                          ContentUploudView,
                                          LogoutView,
                                          ProfileDetailView,
                                          get_trend_videos,
                                          UpdateContent,
                                          get_user_category_contents,
                                          dislike,
                                          GetUserFollowers,
                                          get_content_likes,
                                          PasswordChangeView,
                                          SettingsView,
                                          GetUserCommentarion,
                                          commentarion_delete_view)



from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginView.as_view(),name='login'),
    path('register/', UserRegisterView.as_view(), name='sign_up'),
    path('content_search/', SearchContent.as_view(), name='search'),
    path('comments/<int:pk>/', CommentView.as_view(), name='commentarion_uploud'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile_componenets_change/', UpdateUserProfile.as_view(), name='profile_change'),
    path('like/<int:pk>/', LikeButton.as_view(), name='like'),
    path('profile_photo/', ProfilePhotoView.as_view(), name='photo'),
    path('subscribe/<int:pk>/', SubscribeToUserView.as_view(), name='follow'),
    path('content_delete/<int:pk>/', ContentDeleteView.as_view(), name='delete'),
    path('content_detail/<int:pk>/', ContentDetailView.as_view(), name='detail'),
    path('content/', ContentUploudView.as_view(), name='content'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='user_profiles'),
    path('trend_video/', get_trend_videos, name='trend'),
    path('content_update/<int:pk>/', UpdateContent.as_view(), name='update'),
    path('ineresing_videos/', get_user_category_contents, name='get_user_category_contents'),
    path('dis_like/<int:pk>/', dislike ,name='dont_like'),
    path('user_follwers/<int:pk>/', GetUserFollowers.as_view() ,name='followers'),
    path('get_likes/<int:pk>/', get_content_likes, name='user_likes'),
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('settings/', SettingsView.as_view(), name='settings_components'),
    path('comments/', GetUserCommentarion.as_view(), name='user-comments'),
    path('comments-delete/<int:pk>/', commentarion_delete_view, name='user-comments-delete'),




    # Password Reset

    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirum'),
    # path('password-change/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-change/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),









]