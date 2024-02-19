from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student_Data(models.Model):
    student_name = models.CharField(max_length=255)
    register_number = models.CharField(max_length=20, primary_key=True)
    student_email = models.EmailField()
    borrowed_books_count = models.IntegerField(default=0)
    borrowal_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.student_name

class Borrowed_Book(models.Model):
    borrower = models.ForeignKey(Student_Data, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=20,primary_key=True)
    book_name = models.CharField(max_length=255)
    borrowed_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower.student_name} - {self.book_name}"