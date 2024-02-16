from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *
# Create your views here.

def home(request):
    return render(request, 'library_api/home.html')

class Student_Data_View(viewsets.ModelViewSet):
    queryset = Student_Data.objects.all()
    serializer_class = Student_Data_Serializer

class Borrowed_Book_View(viewsets.ModelViewSet):
    queryset = Borrowed_Book.objects.all()
    serializer_class = Borrowed_Book_Serializer