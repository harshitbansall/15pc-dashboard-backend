from django.urls import path

from .views import (Config, ObtainAuthToken, ObtainAuthTokenGoogleLogin,
                    UserCreate)

urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='token_create'),
    path('googlelogin', ObtainAuthTokenGoogleLogin.as_view(), name='token_create_google'),
    path('signup', UserCreate.as_view(), name='userCreate'),
    path('config', Config.as_view(), name='Config'),


]
