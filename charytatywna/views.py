from django.contrib import messages
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterForm, LoginForm, DonationMultiForm
from django.contrib.auth import authenticate, login
from .models import Donation, Institution, CustomUser, Category


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('landing_page')


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('login')


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
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('landing_page'))
            else:
                messages.error(request, 'Nieprawidłowy email lub hasło.')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Nie ma takiego użytkownika.')
            return redirect(reverse('register'))


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
    form_class = DonationMultiForm
    template_form = 'form.html'
    template_form_confirmation = 'form_confirmation.html'

    def get(self, request, step=1):
        donations_models = Donation.objects.all()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        # form = self.form_class(initial={'key': 'value'})
        if 'donation_data' not in request.session:
            request.session['donation_data'] = {}
        form = self.form_class(initial=request.session.get('donation_data').get('step_' + str(step)))
        return render(request, self.template_form, {'form': form,
                                                    'step': step,
                                                    'donations_models': donations_models,
                                                    'categories': categories,
                                                    'institutions': institutions})

    def post(self, request, step=1):
        donations_models = Donation.objects.all()
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['donation_data']['step_' + str(step)] = form.cleaned_data
            if step == 5:
                donation = Donation.objects.create(**request.session.get('donation_data'))
                return render(request, self.template_form,
                              {'donation_data': request.session.get('donation_data')})
            else:
                return redirect('add_donation', step=step + 1)
        else:
            return render(request, self.template_form, {'form': form,
                                                        'step': step,
                                                        'donations_models': donations_models,
                                                        'errors': form.errors})

    def on_submit(self, request):
        donation = Donation.objects.create(**request.session.get('donation_data'))
        return render(request, self.template_form_confirmation)
