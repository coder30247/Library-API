from rest_framework import serializers
from .models import *


class Student_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Data
        fields = ['student_name', 'register_number', 'student_email', 'borrowed_books_count','borrowal_fine']

class Borrowed_Book_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowed_Book
        fields = ['borrower', 'book_id', 'book_name', 'borrowed_date', 'return_date']

    