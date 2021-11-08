from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser


def login(request):
    title = "Вход"
    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request=request, user=user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse('main'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def edit(request):
    title = "Редактирование"

    if request.method == 'POST':

        edit_form = ShopUserEditForm(data=request.POST,
                                     files=request.FILES,
                                     instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'title': title,
        'edit_form': edit_form,
    }
    return render(request, 'edit.html', context)


def register(request):
    title = "Регистрация"

    if request.method == 'POST':

        register_form = ShopUserRegisterForm(data=request.POST,
                                             files=request.FILES)
        if register_form.is_valid():

            user = register_form.save()

            if send_verify_mail(user):
                messages.add_message(request, messages.SUCCESS, f'Отправили письмо к Вам нам на почту. '
                                                                f'Перейдите по ссылке из письма для активации вашего '
                                                                f'аккаунта!')
                print('-------- EMAIL SENT --------')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('-------- EMAIL SENDING ERROR --------')
                return HttpResponseRedirect(reverse('auth:login'))

    else:

        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form,
    }

    return render(request, 'register.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке:' \
              f'\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_expired():
            user.is_active = True
            user.save()
            auth.login(request=request, user=user)
            return render(request, template_name='verification.html')

        print(f'UserActivations error {user}')
        return render(request, template_name='verification.html')

    except Exception as e:
        print(f'UserVerify error {e.args}')
        return HttpResponseRedirect(reverse('main'))
