from rest_framework import serializers
from .models import *


class Student_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Data
        fields = '__all__'

class Borrowed_Book_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowed_Book
        fields = '__all__'
