import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status

# Create your views here.


def login_view(request):
    context = {}
    return render(request, "login.html", context=context)


def register_view(request):
    context = {}
    return render(request, "register.html", context=context)


def profile_view(request):
    context = {}
    return render(request, "profile.html", context=context)


def collections_view(request):
    context = {}
    return render(request, "collections.html", context=context)


def collection_view(request, collection_id=None):
    context = {"collection_id": collection_id}
    return render(request, 'collection.html', context=context)


def health(_request):
    return HttpResponse(json.dumps({"success": True, "message": "Up and running!"}), status=status.HTTP_200_OK)
