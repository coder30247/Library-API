from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class StudentData(models.Model):
    student_name = models.CharField(max_length=255)
    register_number = models.CharField(max_length=20, unique=True)
    student_email = models.EmailField()
    borrowed_books_count = models.IntegerField(default=0)
    borrowal_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.student_name

class BorrowedBook(models.Model):
    borrower = models.ForeignKey(StudentData, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=20)
    book_name = models.CharField(max_length=255)
    borrowed_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.book_name
