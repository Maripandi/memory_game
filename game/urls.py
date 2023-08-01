from django.urls import path
from game import views
urlpatterns = [
    path('',views.authLogin,name='auth-login'),
    #path('auth-login',views.authLogin,name='auth-login'),
    path('auth-register',views.authRegister,name='auth-register'),
    path('login-validation',views.loginValidation,name='login-validation'),
    path('do-login',views.doLogin,name='do-login'),
    path('register-validation',views.registerValidation,name='register-validation'),
    path('do-register',views.doRegister,name='do-register'),

    path('logout',views.logoutPage,name='log-out'),
    path('home',views.home,name='home'),

    path('game',views.game,name='game'),
    path('game-validator',views.gameValidator,name='game-validator'),

    path('profile',views.profile,name='profile')


    # path('login',views.loginPage,name='login-page'),
    
    # path('register',views.registerPage,name='register'),


]