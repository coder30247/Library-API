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

    # ADDS DATA to the borrowed book table (create)
    # methods=['post'] specifies that this action only responds to POST requests
    @action(detail=False, methods=['post'])
    def add_borrowed_book(self, request):
        try:
            # Extract the student ID and book ID from the request data
            student_id = request.data.get('student')
            book_id = request.data.get('book')

            # Check if the provided student and book exist
            try:
                student = Student_Data.objects.get(id=student_id)
            except Student_Data.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            # Calculate borrowal and return dates
            borrowal_date = datetime.now().date()
            return_date = borrowal_date + timedelta(days=14)

            # Create a new Borrowed_Book instance with the provided data
            borrowed_book_data = {
                'borrower': {'register_number': student_id, 'student_name': student.student_name},  # Nested data
                'book_id': book_id,
                'book_name': book.book_name,
                'borrowed_date': borrowal_date,  # Set the borrow date
                'return_date': return_date,  # Set the return date to 14 days from borrowal date
            }

            # Create a serializer instance with the data from the request
            serializer = Borrowed_Book_Serializer(data=borrowed_book_data)

            # Validate the data using the serializer
            if serializer.is_valid():
                # Save the valid data to the database
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return an error response with the validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return an error response if any exception occurs during the process
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # Retrieve the borrowed book instance with additional details
    @action(detail=True, methods=['get'])
    def retrieve_borrowed_book(self, request, pk=None):
        try:
            # Retrieve the borrowed book instance
            borrowed_book_instance = self.get_object()

            # Serialize the borrowed book data with additional details
            borrowed_book_data = Borrowed_Book_Serializer(borrowed_book_instance).data

            # Calculate the number of days between the return date and the current date
            current_date = datetime.now().date()
            return_date = borrowed_book_instance.return_date
            days_difference = (current_date - return_date).days

            # Show the fine amount only if the book is overdue
            fine_amount = max(days_difference * 0.5, 0)  # Fine is 0 for non-overdue books
            borrowed_book_data['fine_amount'] = fine_amount

            return Response(borrowed_book_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



    
    # Update the borrowed book instance by calculating fine amount and setting return date
    @action(detail=True, methods=['put'])
    def update_return_date(self, request, pk=None):
        try:
            # Retrieve the borrowed book instance
            borrowed_book_instance = self.get_object()

            # Check if the current date is after the return date
            current_date = datetime.now().date()
            if current_date > borrowed_book_instance.return_date:
                # Calculate the fine amount based on the number of days overdue
                days_overdue = (current_date - borrowed_book_instance.return_date).days
                fine_amount = days_overdue * 0.5

                # Add the fine amount to the student's borrowal fine
                student = borrowed_book_instance.borrower
                student.borrowal_fine += fine_amount
                student.save()

            # Update the return date of the borrowed book instance
            return_date = current_date + timedelta(days=14)
            borrowed_book_instance.return_date = return_date
            borrowed_book_instance.save()

            # Serialize the updated borrowed book data
            borrowed_book_data = Borrowed_Book_Serializer(borrowed_book_instance).data

            return Response(borrowed_book_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # delete the borrowed book instance and update the fine
    def return_borrowed_book(self, request, pk=None):
        try:
            # Retrieve the borrowed book instance
            borrowed_book_instance = self.get_object()

            # Calculate the number of days between the return date and the current date
            current_date = datetime.now().date()
            return_date = borrowed_book_instance.return_date
            days_difference = (current_date - return_date).days

            # Show the fine amount only if the book is overdue
            fine_amount = max(days_difference * 0.5, 0)  # Fine is 0 for non-overdue books

            # Add the fine amount to the student's borrowal fine
            student = borrowed_book_instance.borrower
            student.borrowal_fine += fine_amount
            student.save()

            # Delete the borrowed book instance
            borrowed_book_instance.delete()

            return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
