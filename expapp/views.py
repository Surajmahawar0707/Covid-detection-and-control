from django.contrib.messages.api import info
from expapp.models import *
from django.shortcuts import render, redirect
from expapp.forms import usercreateform, dataform
from django.contrib.auth import authenticate, login as auth_login, logout as logout_user
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from PIL import Image

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


@login_required
def contact_after_login(request):
    return render(request, 'contact_after_login.html')


@login_required
def about_after_login(request):
    return render(request, 'about_after_login.html')

def register(request):
    if request.method == 'POST' or request.method == 'FILES':
        form2 = UserCreationForm(request.POST)
        form = usercreateform(request.POST, request.FILES)
        if form2.is_valid() and form.is_valid():
            form = form.save(commit=False)
            form.username = request.POST.get("username")
            form.picture = request.FILES.get("picture")
            form2.save()
            form.save()
            message = "Your account has been created, please login from here..."
            return render(request, 'login.html', {"message": message})
        else:
            datas = request.POST
            message = ''
            if request.POST.get("password1") != request.POST.get("password2"):
                message = "Password validation failed!"
            else:
                message = "Username is already taken!"
            return render(request, 'register.html', {"datas" : datas, "message": message})
    else:
        form1 = usercreateform()
        form2 = UserCreationForm()
        return render(request, 'register.html', {"form1": form1, "form2": form2})


temp_user = ''


def forgot_password(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        global temp_user
        try:
            user = User.objects.get(username = uname)
            temp_user = uname
            if user is not None:
                return redirect('password_reset')
            else:
                message = "username is not valid..."
                return render(request, 'forgot_password.html', {"message" : message})
        except:
            message = "username is not valid..."
            return render(request, 'forgot_password.html', {"message" : message})
    return render(request, 'forgot_password.html')


message_after_password_reset = ''


def password_reset(request):
    global temp_user, message_after_password_reset
    if request.method == "POST":
        user = User.objects.get(username = temp_user)
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
            message_after_password_reset = "password reset successfully!"
            return redirect('login')
        else:
            message = "Both passwords should be same..."
            return render(request, 'password_reset.html', {"message" : message})
    return render(request, 'password_reset.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('input_view')
        else:
            message = "Username or password is incorrect!"
            return render(request, 'login.html', {"message" : message})
    global message_after_password_reset
    if len(message_after_password_reset) > 0:
        m = message_after_password_reset
        message_after_password_reset = ''
        return render(request, 'login.html', {"message" : m})
    else:
        return render(request, 'login.html')


@login_required
def profile_view(request):
    form = usercreateform()
    try:
        if usercreatemodel.objects.get(username = request.user):
            return redirect('input_view')
    except:
        if request.method == 'POST':
            form = usercreateform(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.username = request.user
                form.save()
                return redirect('input_view')
            else:
                messages.info(request, "Data unsuccessful! Please provide right data.")
    return render(request, 'profile.html', {"form": form})


def power(x, o):
    if o == 0:
        return 0
    y = 1
    for i in range(0, o):
        y = y*x
    return y


@login_required
def output_view(request):
        alldata = usercreatemodel.objects.all()
        user_data = usercreatemodel.objects.get(username=request.user)
        values = data.objects.get(username=request.user)
        symp = values.symptoms
        if symp == "None":
            sympbool = 0
        else:
            sympbool = 1
        c_t = values.contact_tracing
        lamb = [random.randint(0,1) for i in range(c_t)]
        omega = [random.random().__round__(2) for i in range(c_t)]
        c = [random.random().__round__(2) for i in range(c_t)]
        mu = [lamb[i]*omega[i] for i in range(c_t)]
        x = 'Probability of users, you have met: '
        x += ' '.join([" | "+str(c[i]) for i in range(c_t)])
        x += ' |'
        y = "Their Infection Transition Factors: "
        y += ' '.join([" | "+str(mu[i]) for i in range(c_t)])
        y += ' |'
        prob = 0
        symp_tell = ""
        for j in range(0, c_t):
            prob += c[j]*mu[j] if c[j] > 0.4 else 0
        prob = min(1, prob)
        w = sympbool*(1 - prob)*0.9
        final_Probability = (prob + w).__round__(2)
        current_stage = 0
        stage_explanation = ""
        if final_Probability == 0:
            current_stage = 0
            stage_explanation += "You are safe, No need to worry ;)"
        elif (final_Probability > 0) and (final_Probability <= 0.40):
            current_stage = 1
            stage_explanation += "Little bit Risk, you may go for a lab test :)"
        elif (final_Probability > 0.40) and (final_Probability < 0.60):
            current_stage = 2
            stage_explanation += "More Risk, You should go for a lab test :("
        elif (final_Probability > 0.60) and (final_Probability < 0.90):
            current_stage = 3
            stage_explanation += "High Risk, You must go for a lab test :("
        else:
            current_stage = 4
            stage_explanation += "You are most probabily infected by Covid-19. Take all precautions and don't get in touch with anyone!"
        if sympbool == 1:
            symp_tell += "You're having serious virus symptoms, must take all precautions and don't get in touch with anyone. Just go for a lab test or stay home."
        else:
            symp_tell += "You're not having any serious symptoms, so chances are little bit low, but take all precautions."
        infected_users_in_district = 0
        infected_users_in_state = 0
        infected_users_in_country = 0
        all_users = output.objects.all()
        curr_district = user_data.district
        curr_state = user_data.state
        curr_country = user_data.country
        for users in all_users:
            userx = usercreatemodel.objects.get(username=users.username)
            if users.probability >= 0.9 and curr_district == userx.district:
                infected_users_in_district += 1
            if users.probability >= 0.9 and curr_state == userx.state:
                infected_users_in_state += 1
            if users.probability >= 0.9 and curr_country == userx.country:
                infected_users_in_country += 1
        try:
            if output.objects.get(username=request.user):
                model = output()
                u = output.objects.get(username=request.user)
                u.delete()
                model.username = request.user
                model.symptoms = symp
                model.contact_tracing = c_t
                model.probability = final_Probability
                model.stage = current_stage
                model.inf_users_in_dis = infected_users_in_district
                model.inf_users_in_state = infected_users_in_state
                model.inf_users_in_cou = infected_users_in_country
                model.save()
        except:
            model = output()
            model.username = request.user
            model.symptoms = symp
            model.contact_tracing = c_t
            model.probability = final_Probability
            model.stage = current_stage
            model.inf_users_in_dis = infected_users_in_district
            model.inf_users_in_state = infected_users_in_state
            model.inf_users_in_coun = infected_users_in_country
            model.save()
        return render(request, 'output.html', {'symp': symp, "x": x, "y": y, "c_t": c_t, "final_prob": final_Probability, "curr_stage": current_stage, "stage_ex": stage_explanation, "district_inf": infected_users_in_district, "state_inf": infected_users_in_state, "country_inf": infected_users_in_country, "symp_tell": symp_tell})


@login_required
def input_view(request):
    form = dataform()
    if request.method == 'POST':
        try:
            curr_user = data.objects.get(username=request.user)
            form = dataform(request.POST or None, instance=curr_user)
            if form.is_valid():
                form.save()
                return redirect('output_view')
            else:
                messages.info(request, "Data uploading unsuccessful! Please provide right data.")
                return render(request, 'input.html')
        except:
            form = dataform(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.username = request.user
                form.save()
                return redirect('output_view')
            else:
                messages.info(request, "Data uploading unsuccessful! Please provide right data.")
                return render(request, 'input.html')
    all_users = usercreatemodel.objects.all()
    user_inf = usercreatemodel.objects.get(username=request.user)
    return render(request, 'input.html', {"form": form, "user_inf": user_inf})




@login_required
def edit_profile(request):
    if request.method == 'POST':
        curr_user = usercreatemodel.objects.get(username=request.user)
        form = usercreateform(request.POST, request.FILES, instance=curr_user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
        else:
            messages.info(request, "data uploading unsuccessful! Please provide right data.")
            return redirect('edit_profile')
        
    else:
        user_inf = usercreatemodel.objects.get(username=request.user)
        return render(request, 'edit_profile.html', {"user_inf": user_inf})

@login_required
def del_acc(request):
    if request.method == 'POST':
        if request.POST.get('answer') == 'Y':
            curr_user = request.user
            ucm = usercreatemodel.objects.get(username=curr_user)
            ucm.delete()
            try:
                dm = data.objects.get(username=curr_user)
                dm.delete()
            except:
                pass
            try:
                om = output.objects.get(username=curr_user)
                om.delete()
            except:
                pass
            curr_user.delete()
            messages.info(request, "Your account has been deleted.")
            return render(request, 'login.html')
        else:
            messages.info(request, "Please enter 'Y' to delete your account!")
            return render(request, 'del_acc.html')
    else:
        return render(request, 'del_acc.html')


@login_required
def logout(request):
    logout_user(request)
    return redirect('login')