from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from api_versao_5.app.api.acionador_api import AcionadoresAPI
from api_versao_5.valores_globais import var_globais
import threading


@csrf_exempt
def login_usuario(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponse("você já está autenticado.")
        return render(request, 'app/login_usuario.html')
    elif request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/auth/painel-app/")
        return render(request, 'app/login_usuario.html')
        
@csrf_exempt
@login_required(login_url="/auth/login-usuario/")
def painel_app(request):
    if request.method == "GET":
        return render(request, 'app/painel.html')
    elif request.method == "POST":
        if var_globais.CHECK_CONN == True:
            print("######## o cliente já está autenticado com wss da IQOption. ########")
            return render(request, 'app/painel.html', {"autenticado": True})
        else:
            print(request.POST)
            username = str(request.POST.get("username"))
            password = str(request.POST.get("password"))
            auth = AcionadoresAPI.autenticacao_iqoption_api(username, password)
            print(auth)
            if auth[0] == True:
                print(auth)
                threading.Thread(target=AcionadoresAPI.conectar_wss(auth[1]["ssid"])).start()
                return render(request, 'app/painel.html', {"autenticado": True})
            return render(request, 'app/painel.html', {"credenciais_invalidas": True})
        
    
    
