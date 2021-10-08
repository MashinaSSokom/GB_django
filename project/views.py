from django.shortcuts import render


def main(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')
