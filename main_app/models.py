from django.db import models

# 1 случай. Когда встроенный Джанго юзер устраивает, но мы хотим что-то новое в него добавить
# from django.contrib.auth.models import AbstractUser  # AbstractUser -> Основа стандартного Юзера
#
#
# class MyUser(AbstractUser):
#     IIN = models.CharField(max_length=12)
#     premium = models.BooleanField(default=False)

# 2 случай. Когда встроенный Джанго юзер не устраивает, мы хотим написать его с нуля
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# AbstractBaseUser -> Основа для юзера(password, is_active, last_login, ...)
# PermissionsMixin -> Права доступа для юзера(is_superuser, groups, permissions, ...)

# Для нового юзера(Написанного с 0) требуется создать "менеджер"
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)  # self.normalize_email -> Удаляет лишний мусор и все в нижний регистр
        user = self.model(email=email, **extra_fields)  # Создаем Джанго объект юзер без пароля
        user.set_password(password)  # set_password -> Хэширует пароль и записывает его юзеру
        user.save()  # save() -> Сохранить юзера в БД
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # unique=True -> Проверяет чтобы не было повторений значений этого поля
    IIN = models.CharField(max_length=12)
    premium = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # USERNAME_FIELD -> Какое поле использовать для авторизации
    REQUIRED_FIELDS = []  # REQUIRED_FIELDS -> Поля, обязательные для создания юзера

    objects = MyUserManager()  # Привязываем MyUserManager к нашему MyUser
