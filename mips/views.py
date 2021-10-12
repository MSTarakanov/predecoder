from django.shortcuts import render
from django.http import HttpResponse
from .forms import BytesField

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = BytesField(request.POST)
        bytes_string = "abdc"
        # bytes_string = form.text
        if form.is_valid():
            bytes_string = form.cleaned_data['text']
        error_title = error_for_bytes_string(bytes_string)
    else:
        form = BytesField()
        error_title = "None"
    return render(request, 'mips/mips_main.html', {'error_title': error_title, 'form': form})


def error_for_bytes_string(string):
    print(string)
    if len(string) % 2 == 0:
        return "Ошибка"
    return "None"


def show_example(request, example_id):
    if example_id == 1:
        form = BytesField(initial={'text': 'a1090000210800022129ffff0129001808100005'})
    elif example_id == 2:
        form = BytesField(initial={'text': 'asrfs'})
    else:
        form = BytesField()
    error_title = "None"
    return render(request, 'mips/mips_main.html', {'error_title': error_title, 'form': form})
