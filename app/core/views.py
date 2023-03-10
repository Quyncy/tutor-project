from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login,logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework import status

from .forms import (
    DozentForm, BlattForm, KursleiterForm,
    LoginForm, KursForm,TutorForm, 
    AuthenticationForm, CostumUserCreationForm, 
    )

import requests, json

# @login_required
# def addToTutorGroup(request):
#     group = Group.objects.get(name='Tutor')
#     request.user.groups.add(group)
#     return HttpResponse("ERfolgreich hinzugefügt")



@login_required(login_url='/login')     # der user muss eingeloggt sein und diese permission bsitzen um diese Seite zu sehen
@permission_required('core.view_core')  # app_label permission
def Index(request):
    return render(request, 'user/index-admin.html')


def login_view(request):
    if request.POST:
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('core views.py: login')
            print(username)
            print(password)

            user = authenticate(username=username, password=password)
            print('user: ')
            print(user)
            if user is not None:
                login(request, user)
                print("login():   ------------")
                print(login(request, user))
                url = 'http://127.0.0.1:8000/accounts/login/'
                payload={
                    'username': username,
                    'password': password,
                }
                print(payload)
                response = requests.post(url, data=payload)

                if response.status_code == 200:
                    print('Yeai')
                    return redirect('index-admin')
    
        #     if user is not None and user.is_admin:
        #         login(request, user)
        #         print(login(request, user))
        #         return redirect('index-admin')
        #     elif user is not None and user.is_tutor:
        #         login(request, user)
        #         print('2')
        #         # return redirect('index-tutor')
        #     elif user is not None and user.is_kursleiter:
        #         login(request, user)
        #         print('3')
        #         # return redirect('index-kursleiter')
        #     else:
        #         pass
        #         # print('Benutzer ist nicht eingeloggt')
        #         # messages.success('Benutzer ist nicht eingeloggt.') 

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form, 'messages': messages})


def logoutView(request):
    logout(request)
    return redirect('login')

# @csrf_protect
# def loginPage(request):
    # form = LoginForm()
    
    # if request.method == "POST":
    #     form = LoginForm(request.POST)

    #     if form.is_valid():
    #         user = auth.authenticate(
    #                 username=form.cleaned_data["email"],
    #                 password=form.cleaned_data["password"])
    #         auth.login(request, user)
    #         return redirect('index')
    #     else:
    #         print('NO')
    #         form = LoginForm()

    # return render(request, 'user/login.html', {'form':form})


@login_required(login_url='/login')
def createUser(request):
    form = CostumUserCreationForm()

    if request.POST:
        url = 'http://127.0.0.1:8000/api/user/create-user/'
        form = CostumUserCreationForm(request.POST)

        if form.is_valid():
            payload={
                'email':form.cleaned_data['email'],
                'vorname':form.cleaned_data['vorname'],
                'nachname':form.cleaned_data['nachname'],
                'rolle':form.cleaned_data['rolle'],
                'is_active':form.cleaned_data['is_active'],
                'is_staff':form.cleaned_data['is_staff'],
                'is_superuser':form.cleaned_data['is_superuser'],
                'is_admin':form.cleaned_data['is_admin'],
                'is_tutor':form.cleaned_data['is_tutor'],
                'is_kursleiter':form.cleaned_data['is_kursleiter'],
                'is_dozent':form.cleaned_data['is_dozent'],
                'password': form.cleaned_data['password1'],
            }
            print(payload)
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                return Response(status=status.HTTP_201_CREATED)
                
    return render(request, 'user/form.html', {'form': form})


def listUser(request):
    url = "http://127.0.0.1:8000/api/user/list-user/"
    response = requests.get(url).json()

    context = {'user': response }
    return render(request, 'user/listUser.html', context)


def get_user_profile(request, id):
    url= f"http://127.0.0.1:8000/api/user/get-user/{id}/"
    user = requests.get(url).json()
    print(user['vorname'])
    context={'user': user}
    return render(request, 'user/get-user-profile.html', context) 






############################


def createKursleiter(request):
    """
    Versenden die Kursleiter Daten an die API
    """
    if request.POST:
        kursleiter_form = KursleiterForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-kursleiter/'

        if kursleiter_form.is_valid():

            payload = {
                # 'email': kursleiter_form.cleaned_data['email'],
                # 'vorname': kursleiter_form.cleaned_data['vorname'],
                # 'nachname': kursleiter_form.cleaned_data['nachname'],
                # 'rolle': 'Kursleiter',
                # 'is_active': kursleiter_form.cleaned_data['is_active'],
                # 'is_staff':kursleiter_form.cleaned_data['is_staff'],
                # 'is_superuser': kursleiter_form.cleaned_data['is_superuser'],
                # # 'groups': kursleiter_form.cleaned_data['groups'],
                # # 'user_permissions': kursleiter_form.cleaned_data['user_permissions'],
                # 'password': make_password(password),
                
                'email': request.POST.get('email'),
                'vorname': request.POST.get('vorname'),
                'nachname': request.POST.get('nachname'),
                'rolle': "Kursleiter",
                'is_active': request.POST.get('is_active'),
                'is_staff': request.POST.get('is_staff'),
                'is_superuser': request.POST.get('is_superuser'),
                'is_admin':request.POST.get('is_admin'),
                'is_tutor':request.POST.get('is_tutor'),
                'is_kursleiter':request.POST.get('is_kursleiter'),
                'is_dozent':request.POST.get('is_dozent'),
                'kurs': request.POST.get('kurs'),
                'password': request.POST.get('password'),
            }
            print('TEST: views.py')
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Kursleiter erfolreich gespeichert.", status=status.HTTP_200_OK)

    kursleiter_form = KursleiterForm()
    # Formular soll Kurse anzeigen
    url = 'http://127.0.0.1:8000/api/kurs/list-kurs/'
    kurse = requests.get(url).json()

    context={'form': kursleiter_form, 'kurse': kurse}
    return render(request, 'user/createkursleiter.html', context)


def listKursleiter(request):
    url = "http://127.0.0.1:8000/api/user/list-kursleiter/"
    response = requests.get(url).json()
    
    context = {'user': response }
    return render(request, 'user/listKursleiter.html', context)


def get_kursleiter_profile(request, id):
    url= f"http://127.0.0.1:8000/api/user/get-kursleiter/{id}/"
    user = requests.get(url).json()

    context={'user': user}
    return render(request, 'user/get-kursleiter-profile.html', context) 


###################

def createTutor(request):
    """
    Versenden die Tutor Daten an die API
    """

    tutor_form = TutorForm()
    # tutorprofile_form = TutorProfileForm()
    url_get_kurs = "http://127.0.0.1:8000/api/kurs/list-kurs/"
    kurs_response = requests.get(url=url_get_kurs).json()

    if request.POST:
        tutor_form = TutorForm(request.POST)
        # tutorprofil_form = TutorProfileForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-tutor/'

        if tutor_form.is_valid():
            # random passwort erstellen
            payload = {
                'email': tutor_form.cleaned_data['email'],
                'vorname': tutor_form.cleaned_data['vorname'],
                'nachname': tutor_form.cleaned_data['nachname'],
                'rolle': tutor_form.cleaned_data['is_active'],
                'is_active':tutor_form.cleaned_data['is_active'],
                'is_tutor':tutor_form.cleaned_data['is_tutor'],
                'tutor_id':tutor_form.cleaned_data['tutor_id'],
                # 'kurs':tutor_form.cleaned_data['kurs'],
                'arbeitsstunden':tutor_form.cleaned_data['arbeitsstunden'],
                'password': tutor_form.cleaned_data['password'],
                # 'is_staff':tutor_form.cleaned_data['is_staff'],
                # 'is_superuser':tutor_form.cleaned_data['is_superuser'],
                # 'is_admin':tutor_form.cleaned_data['is_admin'],
                # 'is_kursleiter':tutor_form.cleaned_data['is_kursleiter'],
                # 'is_dozent':tutor_form.cleaned_data['is_dozent'],
                # 'groups': tutor_form.cleaned_data['groups'],
                # 'user_permissions': tutor_form.cleaned_data['user_permissions'],
            }
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Tutor erfolreich gespeichert.", status=status.HTTP_200_OK)
              
            
    
    context={'form':tutor_form,  'kurse': kurs_response} # 'profile_form':tutorprofile_form,
    return render(request, 'user/createtutor.html', context)



def listTutor(request):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url = "http://127.0.0.1:8000/api/user/list-tutor/"
    response = requests.get(url).json()
    
    context = {'user': response }
    return render(request, 'user/listTutor.html', context)


def get_tutor_profile(request, pk):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url= f"http://127.0.0.1:8000/api/user/get-tutor/{pk}/"
    user = requests.get(url).json()

    context={'user': user}
    return render(request, 'user/get-tutor-profile.html', context) 



####################

def createDozent(request):
    dozent_form = DozentForm()
    
    if request.POST:
        dozent_form = DozentForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-dozent/'

        if dozent_form.is_valid():
            payload = {
                'email': dozent_form.cleaned_data['email'],
                'vorname': dozent_form.cleaned_data['vorname'],
                'nachname': dozent_form.cleaned_data['nachname'],
                'rolle': 'Dozent',
                'is_active': dozent_form.cleaned_data['is_active'],
                'is_staff':dozent_form.cleaned_data['is_staff'],
                'is_superuser': dozent_form.cleaned_data['is_superuser'],
                # 'groups': dozent_form.cleaned_data['groups'],
                # 'user_permissions': dozent_form.cleaned_data['user_permissions'],
                'password': make_password(dozent_form.cleaned_data['password']),
            }
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Dozent erfolreich gespeichert.", status=status.HTTP_200_OK)

    context={'form':dozent_form, }
    return render(request, 'user/createdozent.html', context)


def listDozent(request):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url = "http://127.0.0.1:8000/api/user/list-dozent/"
    response = requests.get(url).json()
    context = {'user': response}
    return render(request, 'user/listDozent.html', context)
    

def get_dozent_profile(request, id):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url= f"http://127.0.0.1:8000/api/user/get-dozent/{id}/"
    user = requests.get(url).json()

    context={'user': user}
    return render(request, 'user/get-dozent-profile.html', context) 



############################

def createKurs(request):
    """
    Verschickt die Kurs Daten an den API Endpoint
    """

    kurs_form = KursForm()

    if request.POST:
        kurs_form = KursForm(request.POST)
        url = 'http://127.0.0.1:8000/api/kurs/create-kurs/'

        if kurs_form.is_valid():
            payload={
                'kurs': kurs_form.cleaned_data['kurs'],
                'beschreibung': kurs_form.cleaned_data['beschreibung'],
                'ref_id': kurs_form.cleaned_data['ref_id'],
            }
            print(payload)
            response = requests.post(url, data=payload)
            if response.status_code ==200:
                return Response(status=status.HTTP_201_CREATED)

    context={'form': kurs_form}
    return render(request, 'user/createkurs.html', context)


def listKurs(request):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url = "http://127.0.0.1:8000/api/kurs/list-kurs/"
    response = requests.get(url).json()
    context = {'kurs': response}
    return render(request, 'user/listKurs.html', context)


def get_kurs_info(request, pk):
    """
    Empfängt die Daten aus der API und zeigt sie im Frontend an
    """
    url = f"http://127.0.0.1:8000/api/kurs/get-kurs/{pk}"
    response = requests.get(url).json()

    context={'kurs': response}
    return render(request, 'user/get-kurs-info.html', context)


##################


def createBlatt(request):
    """
    Verschickt die Daten des Übungsblatts an die API
    """
    blatt_form = BlattForm

    if request.POST:
        blatt_form = BlattForm(request.POST)
        url = 'http://localhost:8000/api/kurs/create-blatt/'

        if blatt_form.is_valid():
            payload = {
                'ass_name': blatt_form.cleaned_data['ass_name'],
                'ass_id': blatt_form.cleaned_data['ass_id'],
                'kurs': blatt_form.cleaned_data['kurs'].id,
            }

            response = requests.post(url, data=payload) # versendet die Daten an den API endpoint
            if response.status_code == '200':
                return Response(status=status.HTTP_200_OK)
    
    context={'form': blatt_form, }
    return render(request, 'user/createblatt.html', context)


def listBlatt(request):
    """
    Empfängt die Liste von Übungsblättern aus der API und zeigt sie im Frontend an
    """
    url = 'http://127.0.0.1:8000/api/kurs/list-blatt/'
    response = requests.get(url).json()
    return render(request, 'user/listBlatt.html', {'blatt': response})


def get_blatt_info(request, pk):
    """
    Empfängt die Übungsblatt Informationen aus der API und zeigt sie im Frontend an
    """
    url = f"http://127.0.0.1:8000/api/kurs/get-blatt/{pk}"
    response = requests.get(url).json()

    if request.method == 'PUT':
        blatt = BlattForm(request.POST)
        # erhalte Daten aus dem Formular und sende es an die API
        request.put(url)

    elif request.method == 'DELETE':
        requests.delete(url)

    context = {'blatt': response}
    return render(request, 'user/get-blatt-info.html', context)


##################################
