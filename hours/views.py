# from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi! You're at the volunteer hours index.")
