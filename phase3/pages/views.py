from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import *
from pages.urls import *
import re
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def Home_page(request):
    return render(request, "pages/Home_page.html", {"name": "Home_page"})


def SignUp_page(request):
    if request.method == "POST":
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        user = request.POST.get("username")
        passw = request.POST.get("password")
        em = request.POST.get("email")
        confirm_pass = request.POST.get("confirm-password")
        type = request.POST.get("Type")

        if SignUp.objects.filter(usernamee=user).exists():
            return HttpResponse(
                "Username already exists. Please choose a different one."
            )
            # x = True
            # alert_script = f'''
            #    <script>
            #        if ({'true' if x else 'false'}) {{
            #             alert("Your first alert message goes here");
            #      }}
            #     </script>
            #     '''
            # return render(request, 'pages/Sign_up.html', {'alert_script': alert_script})

        if SignUp.objects.filter(Email=em).exists():
            return HttpResponse(
                "Email already exists. Please Log in or use a different one."
            )

        if passw != confirm_pass:
            return HttpResponse("Password isn't the same as confirm password")

        password_strength = validate_password_strength(passw)
        if password_strength != True:
            return HttpResponse(
                "Password strength requirements not met: "
                + ", ".join(password_strength)
            )

        if user and em:
            try:
                data = SignUp(
                    FirstName=fname,
                    LastName=lname,
                    usernamee=user,
                    Password=passw,
                    Email=em,
                    AccType=type,
                )
                data.save()
                return Login_page(request)
            except Exception as e:
                return HttpResponse("Error occurred while signing up: " + str(e))
    return render(request, "pages/Sign_up.html", {"name": "Sign_up"})


def validate_password_strength(value):
    reasons = []
    if len(value) < 8:
        reasons.append("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", value):
        reasons.append("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        reasons.append("Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        reasons.append("Password must contain at least one number")
    return reasons if reasons else True


def Login_page(request):
    if request.method == "POST":
        user = request.POST.get("username")
        passw = request.POST.get("password")

        if user and passw:
            try:
                if SignUp.objects.filter(usernamee=user).exists():
                    accoutType = SignUp.objects.get(usernamee=user, Password=passw)

                    if accoutType.AccType == "Admin":
                        return AdminHome_page(request)

                    elif accoutType.AccType == "User":
                        return UserHome_page(request)
            except SignUp.DoesNotExist:
                return HttpResponse("Invalid username or password")
    return render(request, "pages/Log_in.html", {"name": "Log_in"})


def AdminHome_page(request):
    return render(request, "pages/Admin_home_page.html", {"name": "AdminHome"})


def UserHome_page(request):
    return render(request, "pages/User_home_page.html", {"name": "UserHome"})


def AdminList_page(request):
    return render(request, "books/View_list_admin.html", {"book": Book.objects.all()})


def BookDetails_Admin(request):
    book_id = request.GET.get("id")
    book = get_object_or_404(Book, id=book_id)
    return render(request, "books/view.html", {"book": book})


def UserList_page(request):
    return render(request, "books/View_list_user.html", {"book": Book.objects.all()})


def BookDetails_User(request):
    book_id = request.GET.get("id")
    book = get_object_or_404(Book, id=book_id)
    return render(request, "books/BookDetailsUser.html", {"book": book})


def add_book(request):
    if request.method == "POST":
        Id = request.POST.get("book_id")
        Name = request.POST.get("book_name")
        Author = request.POST.get("author")
        Category = request.POST.get("category")
        Description = request.POST.get("description")
        PublishDate = request.POST.get("publish_date")
        CoverImage = request.FILES.get("book_image")
        if Id:
            data = Book(
                bId=Id,
                bName=Name,
                bAuthor=Author,
                bCategory=Category,
                bDescription=Description,
                bPublishDate=PublishDate,
                bCoverImage=CoverImage,
            )
            data.save()
            return AdminList_page(request)
        else:
            return Addbook_page(request)
    else:
        return AdminHome_page(request)


def Addbook_page(request):
    return render(request, "books/Add_books.html", {"name": "AddBook"})

@csrf_exempt
def delete_book(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")

        try:
            book_to_delete = Book.objects.get(pk=book_id)
            book_to_delete.delete()
            return JsonResponse({"message": "Book deleted successfully"}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)




def update_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        new_author = request.POST.get('new_author')
        new_genre = request.POST.get('new_genre')
        new_description = request.POST.get('new_description')

        # Retrieve the book instance
        book = get_object_or_404(Book, pk=book_id)

        # Update book attributes
        book.bAuthor = new_author
        book.bCategory = new_genre
        book.bDescription = new_description

        try:
            book.save()
            return JsonResponse({'message': 'Book details updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def search_books(request):
    query = request.GET.get('query', '')
    if query:
        books = Book.objects.filter(bName__icontains=query) | Book.objects.filter(bAuthor__icontains=query)
        suggestions = [{'id': book.id, 'title': book.bName, 'author': book.bAuthor, 'cover_image_url': book.bCoverImage.url} for book in books]
    else:
        suggestions = []
    return JsonResponse({'suggestions': suggestions})

def search_page(request):
    return render(request, 'search_page.html')



def filter_books(request):
    category = request.GET.get('category', 'All')
    if category == 'All':
        books = Book.objects.all()
    else:
        books = Book.objects.filter(bCategory=category)

    serialized_books = [{'id': book.id, 'title': book.bName, 'author': book.bAuthor, 'cover_image_url': book.bCoverImage.url, 'category': book.bCategory, 'publish_date': book.bPublishDate} for book in books]
    return JsonResponse({'books': serialized_books})

def Borrowing(request):
    book_id = request.GET.get('id')  
    book = get_object_or_404(Book, id=book_id)
    return render(request, "books/Borrowing.html", {"book": book})

def BorrowedBooks(request):
    borrowed_books = [] 
    return render(request, "books/Borrowed_list.html", {"borrowed_books": borrowed_books})

def process_borrow(request):
    if request.method == "POST":
        book_id = request.POST.get("id")
        date = request.POST.get("Date")
        time = request.POST.get("Time")
        duration = request.POST.get("Duration")
        return redirect('BorrowedBooks')
    return redirect('BorrowBook')
