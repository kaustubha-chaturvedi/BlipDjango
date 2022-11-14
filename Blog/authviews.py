from django.contrib.sites.shortcuts import get_current_site
from .models import *
from .forms import*
from django.contrib import messages
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                
                current_site = get_current_site(request)
                mail_subject = 'Activate your Blip account.'
                message = render_to_string('auth/email_template.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk))  ,
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Form submission successful Activation Link Was sent to email')
                return HttpResponseRedirect('/signin')
        else:
            form = SignUpForm()
        return render(request, 'auth/signup.html', {'form':form,'site':SiteDescription.objects.all()})
    else:
        return HttpResponseRedirect('/admin')

def user_activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Account Activated')
        return HttpResponseRedirect('/signin')
    else:
        messages.success(request,'Activation link is invalid!')
        return HttpResponseRedirect('/signup')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=email,password=upass)
                if user is not None:
                    login(request,user)
                    messages.error(request,"Loggeg in Successfully")
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request,"User doesn't exist")
                    return HttpResponseRedirect('/')
            else:
                messages.error(request,"User doesn't exist")
                return HttpResponseRedirect('/')     
        else:
            form = LoginForm()
            return render(request, 'auth/login.html',{'form':form,'site':SiteDescription.objects.all()})
    else:
        return HttpResponseRedirect('/admin')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

