from django.shortcuts import render


def main(request):
    context = {'title': 'Главная'}

    return render(request, 'index.html', context=context)


def contacts(request):
    context = {'title': 'Контакты'}

    return render(request, 'contacts.html', context=context)
