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
    

    def list(self, request, *args, **kwargs):
        # Get the original response from the parent class
        response = super().list(request, *args, **kwargs)

        # Enhance the response by adding borrowed books for each student
        student_data = response.data
        enhanced_data = []

        for student in student_data:
            student_instance = Student_Data.objects.get(pk=student['register_number'])
            borrowed_books = Borrowed_Book.objects.filter(borrower=student_instance)
            borrowed_books_data = Borrowed_Book_Serializer(borrowed_books, many=True).data

            student['borrowed_books'] = borrowed_books_data
            enhanced_data.append(student)

        # Update the response data
        response.data = enhanced_data

        return response


class Borrowed_Book_View(viewsets.ModelViewSet):
    queryset = Borrowed_Book.objects.all()
    serializer_class = Borrowed_Book_Serializer