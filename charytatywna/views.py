from django.shortcuts import render, redirect
from django.views import View
from .forms import DonationForm, RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
class LandingPageView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)


class AddDonationView(View):
    template_name = 'form.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')

        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})