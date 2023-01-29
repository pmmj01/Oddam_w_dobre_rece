from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm, DonationMultiForm, UserEditForm
from django.contrib.auth import authenticate, login
from .models import Donation, Institution, CustomUser, Category
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .mixins import AjaxFormMixin


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
        total_institution = Donation.objects.values('institution__name').annotate(total=Count('institution__name'))
        # total_institution = Donation.objects.count()
        # total_institution = Donation.objects.values('institution').annotate(total=Coalesce(Count('institution'), 0))

        if total_donations['total'] is None:
            total_donations['total'] = 0
        # if not total_institution:
        #     total_institution = 0

        return render(request, 'index.html',
                      {'total_donations': total_donations, 'total_institution': total_institution})

    def category_count(request):
        donations = Donation.objects.values('category').annotate(total=Count('category'))
        return render(request, 'index.html', {'donations': donations})


# class AddDonationView(LoginRequiredMixin, View):
# form_class = DonationMultiForm
# template_form = 'form.html'
# template_form_confirmation = 'form-confirmation.html'

# def get(self, request):
#     donations_models = Donation.objects.all()
#     categories = Category.objects.all()
#     institutions = Institution.objects.all()
#     donation_data = request.session.get('donation_data')
#     step = int(self.request.GET.get('data-step', 1))
#     if 'donation_data' not in request.session:
#         request.session['donation_data'] = {}
#     form = self.form_class(initial=request.session.get('donation_data').get('step_' + str(step)))
#     if step > 5:
#         step = 5
#     return render(request, self.template_form, {'form': form,
#                                                 'step': step,
#                                                 'donations_models': donations_models,
#                                                 'categories': categories,
#                                                 'institutions': institutions,
#                                                 'donation_data': donation_data})
#
# def post(self, request):
#     step = int(self.request.POST.get('data-step', 1))
#     donations_models = Donation.objects.all()
#     categories = Category.objects.all()
#     institutions = Institution.objects.all()
#     form = self.form_class(request.POST, step=step)
#     if form.is_valid():
#         request.session['donation_data']['step' + str(step)] = form.cleaned_data
#         if step == 5:
#             donation = Donation.objects.create(**request.session.get('donation_data'))
#             form.save()
#             return render(request, self.template_form_confirmation, {'donation': donation,
#                                                         'form': form,
#                                                         'data-step': step,
#                                                         'donations_models': donations_models,
#                                                         'errors': form.errors,
#                                                         'categories': categories,
#                                                         'institutions': institutions})
#         else:
#             if step < 5:
#                 step += 1
#             return redirect('add_donation', step=step+1)
#     else:
#         return redirect(reverse(self.template_form_confirmation))

class AddDonationView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = DonationMultiForm
    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['institution'] = Institution.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        donation = form.save()
        if self.request.is_ajax():
            return JsonResponse({
                'donation': {
                    'category': donation.category.name,
                    'quantity': donation.quantity,
                    'institution': donation.institution.name,
                    'address': donation.address,
                    'phone_number': donation.phone_number,
                    'city': donation.city,
                    'zip_code': donation.zip_code,
                    'pick_up_date': donation.pick_up_date,
                    'pick_up_time': donation.pick_up_time,
                    'pick_up_comment': donation.pick_up_comment,
                }
            })
        return redirect(self.success_url)


class DonationSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserDetails(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user_id=user.id)
        return render(request, 'user_details.html', {'user': user, 'donations': donations})

    def post(self, request):
        confirm = request.POST.get('confirm')
        donation = Donation.objects.get(id=confirm)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('user_details'))


class UserUpdate(LoginRequiredMixin, View):
    template_name = 'user_update.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user': user})

    def post(self, request):
        user = request.user
        if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            return redirect(reverse('user_details'))
        return render(request, self.template_name, {'user': user, 'message': "Wprowadzono niepoprawne hasło!"})


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        user = request.user
        if user.check_password(request.POST.get('old-password')):
            new_password = request.POST.get('new-password')
            new_password2 = request.POST.get('new-password2')
            if new_password == new_password2:
                user.set_password(new_password)
                user.save()
                return redirect(reverse('login'))
            return render(request, 'change_password.html', {'message2': "Nowe hasła nie są takie same!"})
        return render(request, 'change_password.html', {'message': "Stare hasło jest błędne!"})


# class SuperuserRequiredMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_superuser:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)

class SuperuserRequiredMixin(UserPassesTestMixin):
    permission_required = 'auth.view_user'

    def test_func(self):
        return self.request.user.is_superuser


class AdminPanel(SuperuserRequiredMixin, View):
    def get(self, request):
        return redirect('admin_page')


class UserListView(SuperuserRequiredMixin, View):
    def get(self, request):
        users = CustomUser.objects.all()
        context = {'users': users}
        return render(request, 'user_list.html', context)

    @require_http_methods(["PUT"])
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if request.POST['_method'] == 'DELETE':
            user.delete()
            messages.success(request, 'Użytkownik został usunięty')
        elif request.POST['_method'] == 'PUT':
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Użytkownik został zaktualizowany')
                return redirect('user_edit')
        return redirect('user_list')


class UserEditView(SuperuserRequiredMixin, View):
    template_name = 'user_update.html'

    def get(self, request, id):
        obj = get_object_or_404(CustomUser, pk=id)
        form = UserEditForm(initial={
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
        })
        return render(request, self.template_name, locals())

    def post(self, request, id):
        obj = get_object_or_404(CustomUser, pk=id)
        form = UserEditForm(request.POST, initial={
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
        })
        if form.is_valid():
            form.save()
            return redirect('user_list')


class UserDeleteView(SuperuserRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(CustomUser, pk=id)
        user.delete()
        return redirect('user_list')
