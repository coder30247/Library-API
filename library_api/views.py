from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *
# Create your views here.

def home(request):
    return render(request, 'library_api/home.html')

class Student_Data_View(viewsets.ModelViewSet):
    queryset = Student_Data.objects.all()
    serializer_class = Student_Data_Serializer 

    @action(detail=True, methods=['get'])
    def retrieve_student_data(self, request, pk=None):
        # Retrieve the student instance
        student_instance = self.get_object()

        # Serialize the student data
        student_data = Student_Data_Serializer(student_instance).data

        # Get the borrowed books for the student
        borrowed_books = Borrowed_Book.objects.filter(borrower=student_instance)
        
        # Serialize the borrowed books data with additional details
        borrowed_books_data = []
        for book in borrowed_books:
            book_data = Borrowed_Book_Serializer(book).data
            book_data['due_date'] = book.return_date  # Add the due date (replace with the actual field name)
            book_data['fine_amount'] = book.fine_amount  # Add the fine amount (replace with the actual field name)
            borrowed_books_data.append(book_data)

        # Add borrowed books data to the student data
        student_data['borrowed_books'] = borrowed_books_data

        return Response(student_data)
class Borrowed_Book_View(viewsets.ModelViewSet):
    queryset = Borrowed_Book.objects.all()
    serializer_class = Borrowed_Book_Serializer