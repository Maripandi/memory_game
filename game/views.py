from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from game.models import Card,Score,Game
from game.forms import LoginForm,RegisterForm
from game.myMethods import CustomFunctions

import time
import datetime as dt
import json
# Ceate your views here.
cf = CustomFunctions()

loginCount = 0

def authLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        global loginCount
        loginCount = 0
        return render(request,'auth/auth_login.html',{'logform':LoginForm()})

# @csrf_exempt
# def authLoginxxx(request):
#     return render(request,'auth/auth_login.html',{'logform':LoginForm()})

@csrf_exempt
def loginValidation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password =  data['password']
        global loginCount
        if len(username) == 0:
            msg = ['danger','username','field cannot be empty']
        else:
            #print(loginCount)
            if loginCount >= 2:
                msg = ['primary','username or password','is invalid']
            else:
                x = cf.password_validator(password)
                if x == True:
                    msg = ['info','username_and_password',' is valid']
                    global user
                    user = authenticate(username=username,password= password)
                    print(user)
                    if user is not None:
                        msg = ['info','username_and_password',' is valid']
                        #return render(request,)
                    else:
                        loginCount += 1
                        msg = ['danger','username or password','is invalid']                    
                else:
                    msg = ['danger','password','Enter a valid Password']
                    loginCount += 1
        return render(request,'auth/span.html',{'msg':msg})
    else:
        return redirect('auth-page')

@csrf_exempt
def doLogin(request):
    if request.method == 'POST':
        login(request,user)
        msg = ['light',f'hello {user} you are logged in successfully ']
        return render(request,'auth/auth_msg.html',{'msg':msg})
    else:
        return redirect('auth-page')

@csrf_exempt
def authRegister(request):
    return render(request,'auth/auth_register.html',{'regform':RegisterForm()})

@csrf_exempt
def registerValidation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['type'] == 'username':
            username = data['value']
            x = cf.nameValidation('username',username)
            if x == True:
                user_exists = User.objects.filter(username=username).exists()
                if user_exists == True:
                    msg = ['danger','username',f'{username} already exists try a different name']
                else:
                    msg = ['success','username','ok']
                return render(request,'auth/span.html',{'msg':msg })
            else:
                msg = ['danger','username',x]
                return render(request,'auth/span.html',{'msg':msg})
        elif data['type'] == 'password1':
            global password1
            password1 = data['value']
            y = cf.password_validator(password1)
            if y == True:
                msg = ['success','password','ok']
                return render(request,'auth/span.html',{'msg':msg})
            else:
                msg = ['danger','password',y]
                return render(request,'auth/span.html',{'msg':msg})

        elif data['type'] == 'password2':
            password2 = data['value']
            if len(password2) < 8:
                msg = ['danger','password_match','your passwords cannot be lessthen 8 characters']
                return render(request,'auth/span.html',{'msg':msg})
            elif password1 == password2:
                msg = ['success','password_match','ok']
                return render(request,'auth/span.html',{'msg':msg})
            else:
                msg = ['danger','password_match','your password did not match']
                return render(request,'auth/span.html',{'msg':msg})
        else:
            pass
        return redirect('auth-page')
    else:
        return redirect('auth-login')

@csrf_exempt
def doRegister(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        user = User.objects.create_user(username=username,password=password,email=email)
        user.save()
        msg = ['info',f' Hello {username} You are Registred success fully']
        return render(request,'auth/auth_msg.html',{'msg':msg})
    else:
        return redirect('auth-page')

def home(request):
    if request.user.is_authenticated:
        leaders = Score.objects.all().order_by('score')
        # print(cf.leaderboards())
        return render(request,'home.html',{'leaders':reversed(leaders)})
    else:
        return redirect('auth-login')

def logoutPage(request):
    logout(request)
    return redirect ('auth-login')

def game(request):
    if request.user.is_authenticated:
        gamedata = Game.objects.filter(user_id = request.user.id).exists()
        if gamedata == False:
            gd = Game.objects.create(user_id = request.user.id,
                        started_at = dt.datetime.now(), is_completed = False )
            gd.save()
        else:
            gd = Game.objects.filter(user_id = request.user.id,is_completed = False).exists()
            if gd == False:
                gd = Game.objects.create(user_id = request.user.id,is_completed = False )
                gd.save()
        
        global gamevalue1,matchcounter
        gamevalue1 = None
        cards = Card.objects.all()
        matchcounter = cards.count()
        df = cf.shuffedCards2x(cards)
        return render(request,'game/game.html',{'df':df})
    else:
        return redirect('auth-login')

gamevalue1 = None
matchcounter = 0
@csrf_exempt
def gameValidator(request):
    if request.method == 'POST':
        time.sleep(0.7)
        data = json.loads(request.body)
        value = data['value']
        # value = value[1:]
        global gamevalue1,matchcounter
        if gamevalue1:
            gamevalue2 = value
            # print('gamevalue2',gamevalue2)
            if gamevalue1 == gamevalue2:
                gamevalue1 = None
                res = ('Dont click same card again',)
            elif gamevalue1[1:] == gamevalue2[1:]:
                # print(gamevalue1[1:],gamevalue2[1:])
                res = ['match',gamevalue1[1:],gamevalue2[1:]]
                gamevalue1 = None
                matchcounter -= 1
                if matchcounter == 0:
                    res[0]='end'
                    #gd = Game.objects.get(user_id = request.user.id)
                    gd = Game.objects.get(user_id = request.user.id,is_completed = False)
                    gd.is_completed = True
                    gd.ended_at = dt.datetime.now()
                    gd.save()
                    gameCount = Game.objects.filter(user_id = request.user.id,is_completed = True).count()
                    scoredata = Score.objects.filter(user_id = request.user.id).exists()
                    
                    if scoredata == True:
                        sd = Score.objects.get(user_id = request.user.id)
                        sd.score = gameCount
                        sd.created_at = dt.date.today()
                        sd.save()
                    else:
                        sd = Score.objects.create(score = gameCount,user_id = request.user.id)
                        sd.save()
            else:
                res = ('did not match',gamevalue1[1:],gamevalue2[1:])
                gamevalue1 = None
                # print('didnot match',res)
            return render(request,'game/result.html',{'res':res})
        else:
            gamevalue1 = value
            # print('gamevalue1',gamevalue1)
        return render(request,'game/result.html')
    else:
        return redirect('auth-login')



def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        return redirect('auth-login')































def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                msg = ['danger','invalid username or password']
                return render(request,'auth/login.html',{'form':form,'msg':msg})
        else:
            return render(request,'auth/login.html',{'form':form})
    else:
        form = LoginForm()
        return render(request,'auth/login.html',{'form':form})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    return render(request,'auth/register.html',{'form':form})
# def registerValidation(request):
#     msg = ['success','ok']
#     return render(request,'auth/validate_msg.html',{'msg':msg})

