from django.urls import path
from user import views

urlpatterns = [
    path('user/register', views.RegisterAPI.as_view(), name='register'),
    path('user/login', views.LoginAPI.as_view(), name='login'),
    path('user/auth', views.UserAPI.as_view(), name='auth'),
    path('user/logout', views.LogOutAPI.as_view(), name='logout'),
    path('user/validate', views.ValidateAPI.as_view(), name='validate'),
    path('user/forget/password', views.RequestPasswordResetEmailAPI.as_view(), name='forgetPassword'),
    path('user/make/password', views.SetNewPassword.as_view(), name='newPassword'),
    path('user/review/', views.UserReviewAPI.as_view(), name='user/review'),
    path('user/review/<int:pk>/', views.UserReviewAPI.as_view(), name='user/review/pk'),
    path('user/retrieve/<int:pk>/', views.RetrieveUserAPI.as_view(), name='user/retrieve/pk'),
]

# router = DefaultRouter()
#
# router.register('user/review', views.UserReviewAPI, basename='user/review')
# router.register('user/register', views.RegisterAPI.as_view(), basename='user/register')
# router.register('user/login', views.LoginAPI.as_view(), basename='user/login')
# router.register('user/auth', views.UserAPI.as_view(), basename='user/auth')
# router.register('user/logout', views.LogOutAPI.as_view(), basename='user/logout')
# router.register('user/validate', views.ValidateAPI.as_view(), basename='user/validate')
# router.register('user/forget/password', views.RequestPasswordResetEmailAPI.as_view(), basename='user/forget/password')
# router.register('user/make/password', views.SetNewPassword.as_view(), basename='user/make/password')
#
# urlpatterns = router.urls