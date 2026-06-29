from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def counter(request):
    return render(request, 'counter.html')


def make_ten(request):
    return render(request, 'make_ten.html')


def clock(request):
    return render(request, 'clock.html')


def length_units(request):
    return render(request, 'length_units.html')


def rmb(request):
    return render(request, 'rmb.html')


def number_line(request):
    return render(request, 'number_line.html')


def multiplication(request):
    return render(request, 'multiplication.html')


def division(request):
    return render(request, 'division.html')
