import random

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        # Создание пользователя со значением is_active=False
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        # Генерация кода для юзера и запись в БД
        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        new_user.activation_token = token
        new_user.save()
        # Подготовка данных для отправки по электронной почте
        current_site = get_current_site(self.request)
        # Отправка электронной почты
        send_mail(
            subject='Поздравляем вас с регистрацией',
            message=f'Пожалуйста, перейдите по ссылке для активации вашего аккаунта: \n\n'
                    f'http://{current_site.domain}/users/activate/{uid}/{token}/',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
            )
        return super().form_valid(form)


def activate_account(request, activation_token):
    try:
        user = User.objects.get(activation_token=activation_token)
        user.is_active = True
        user.save()
        return redirect(reverse('catalog:homepage'))  # Перенаправление на главную страницу после активации
    except User.DoesNotExist:
        return render(request, 'users/activation_error.html')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:homepage'))

    # def form_valid(self, form):
    #     new_user = form.save()
    #     send_mail(
    #         subject='Поздравляем вас с регистрацией',
    #         message='Вы зарегистрировались на новой платформе, добро пожаловать!',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[new_user.email]
    #     )
    #     return super().form_valid(form)
    #     # return redirect(reverse('catalog:homepage'))