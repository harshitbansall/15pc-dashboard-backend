from django.urls import path

from .views import (Config, ObtainAuthToken, ObtainAuthTokenGoogleLogin,
                    UserCreate, UserCreateGoogle)

urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='token_create'),
    path('googlelogin', ObtainAuthTokenGoogleLogin.as_view(), name='token_create_google'),
    path('googlesignup', UserCreateGoogle.as_view(), name='user_create_google'),
    path('signup', UserCreate.as_view(), name='userCreate'),
    path('config', Config.as_view(), name='Config'),


]
