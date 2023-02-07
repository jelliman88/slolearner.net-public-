from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from .models import UserProfile
from .forms import NewUserForm, UserAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from random import randrange
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os


def homepage(request):
    if request.user.is_authenticated:
        return redirect('learn:dash')
    #trans = translate(language='en')
    return render(request, 'homepage.html')

def sample(request):
    return render(request, 'sample.html')


def verify_email(request):
    msg = ''
    if request.POST:
        user_code = request.POST.get('code')
        user_model = UserProfile.objects.get(email=request.user)

        if user_code == str(user_model.verification_code):
            user_model.is_verified = True
            user_model.verification_code = 0
            user_model.save()
            return redirect('homepage:homepage')
        else:
            msg = 'incorrect code'
    context = {'msg': msg}
    return render(request, 'verify-email.html', context)


def login_form(request):
    if request.user.is_authenticated:
        return redirect('learn:dash')
    if request.method == 'GET':
        return render(request, 'login.html', {'form': UserAuthenticationForm()})
    else:
        user = authenticate(
            request, email=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {'form': UserAuthenticationForm(), 'error': 'username or password incorrect'})
        else:
            login(request, user)
            if request.user.is_superuser:
                return redirect('homepage:homepage')
            else:
                return redirect('learn:dash')


def logout_form(request):
    if request.method == "POST":
        logout(request)
        return redirect('homepage:homepage')


def signup_form(request):
    if request.user.is_authenticated:
        return redirect('user_dash:index')
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': NewUserForm()})
    else:
        # check if email is in focus group -------------------
        focus_string = str(os.getenv('FOCUS_GROUP'))
        focus_group = [x.strip() for x in focus_string.split(',')]
        if request.POST['email'] not in focus_group:
            msg = 'focus-group-error'
            return render(request, 'signup.html', {'form': NewUserForm(), 'error': msg})
        # end check ------------------------
        if request.POST['password1'] == request.POST['password2']:
            try:
                four_digit_code = randrange(1000, 9999)
                language_code = request.POST.get('language-code')
                user = UserProfile.objects.create_user(
                    request.POST['email'], request.POST['username'], password=request.POST['password1'])
                user.verification_code = four_digit_code
                user.website_lang = language_code
                user.save()

                subject = 'Verification Code'
                html_message = render_to_string(
                    'verification-mail-template.html', {'user': user.username, 'code': four_digit_code})
                plain_message = strip_tags(html_message)
                from_email = 'slolearner.net <contact@slolearner.net>'
                to = request.POST['email']
                mail.send_mail(subject, plain_message, from_email, [
                               to], html_message=html_message)
                login(request, user)
 
                return redirect('homepage:verify-email')
            except IntegrityError:
                ValidationError("User with this email already exist")
                return render(request, 'customer/auth/signup.html', {'form': NewUserForm(), 'error': 'account already exists under this email'})

        else:
            return render(request, 'customer/auth/signup.html', {'form': NewUserForm(), 'error': 'passwords did not match'})


def podcast(request):
    return render(request, 'podcast.html')


def translate(language, string):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext(string)
    finally:
        activate(cur_language)
    return text

