from django.contrib import admin
from .models import StudentData, BorrowedBook
# Register your models here.

admin.site.register(StudentData)
admin.site.register(BorrowedBook)