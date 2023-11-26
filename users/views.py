import random

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User


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
        new_user = form.save()
        send_mail(
            subject='Поздравляем вас с регистрацией',
            message='Вы зарегистрировались на новой платформе, добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)
    # def form_valid(self, form):
    #     # Метод, который отрабатывает при успешной валидации формы
    #     if form.is_valid():
    #         self.object = form.save()
    #         # Сохранение объекта перед тем, как установить ему пароль
    #         if form.data.get('need_generate', False):
    #             self.object.set_password(  # Функция установки пароля,
    #                 # которая хеширует строку для того,
    #                 # чтобы не хранить пароль в открытом виде в БД
    #                 self.object.make_random_password(12)  # Функция генерации пароля
    #             )
    #             self.object.save()
    #
    #     return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Высменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:homepage'))