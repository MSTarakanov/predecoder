from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.method == 'POST':
        print(request.POST)
        print("Hello, console!")
        bytes_string = "abdc"
        error_title = error_for_bytes_string(bytes_string)
        return render(request, 'mips/mips_main.html', {'error_title': error_title})
    else:
        return render(request, 'mips/mips_main.html')


def error_for_bytes_string(string):
    if len(string) % 2 == 0:
        return "Ошибка"
    return "None"