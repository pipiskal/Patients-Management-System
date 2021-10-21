from django.shortcuts import render, redirect
from django.http import HttpResponse



def main_page(request):
    if request.method == "GET":
        return render(request, "home.html")
    else:
        return HttpResponse("something went wrong")