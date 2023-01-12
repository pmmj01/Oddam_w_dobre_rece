from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.views import View
from .forms import DonationForm, RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from .models import Donation, Institution

# Create your views here.
class LandingPageView(View):
    template_name = 'index.html'
    def get(self, request):
        total_donations = Donation.objects.aggregate(total=Sum('quantity'))
        total_institution = Donation.objects.values('institution').annotate(total=Count('institution'))
        if total_donations['total'] is None:
            total_donations['total'] = 0
        if not total_institution:
            total_institution = 0
        return render(request, 'index.html',
                      {'total_donations': total_donations, 'total_institution': total_institution})
    def category_count(request):
        donations = Donation.objects.values('category').annotate(total=Count('category'))
        return render(request, 'index.html', {'donations': donations})



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