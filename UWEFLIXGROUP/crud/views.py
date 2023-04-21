from django.shortcuts import render, redirect
from django.contrib.auth import login as login2, authenticate, logout as logout2
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied


from .models import User, Customer, FilmShowings, Film
from .forms import LoginForm, CustomerForm, FilmForm

@login_required(login_url='/auth')
def home(request):
    # Load films
    showings = Film.objects.all()

    return render(request, 'home.html', {'films': showings})


# Generic Authentication Function
def authenticate_account(request):
    # Get the form
    form = LoginForm(request.POST)

    # Check if the form is valid

    if not form.is_valid():
        return None

    # Clean the form data
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    # Check if the login details are correct
    user = authenticate(request, username=email, password=password)

    return user
        

# Customer Login View
def login(request):
    # If the request is POST, then the user has submitted the login form
    if request.method == 'POST':
        # Authenticate the user
        user = authenticate_account(request)

        # If the username/password is correct, log the user in

        if not user:
            return render(request, 'auth/index.html', {'error': 'Invalid username and or password'})

        login2(request, user)

        # Redirect User
        return HttpResponseRedirect('/')


    # If the user is already logged in, redirect them to the home page
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    return render(request, 'auth/index.html')

def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if not form.is_valid():
            return render(request, 'auth/register.html', {'error': f'Invalid form data - {form.errors}'})
        
        data = form.cleaned_data

        # Check for existing email
        if User.objects.filter(email=data['email']).exists():
            return render(request, 'auth/register.html', {'error': 'This E-Mail has already been registered'})

        user = User.objects.create(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            is_customer=True
        )

        user.set_password(data['password'])
        user.save()

        # Create Customer
        customer = Customer.objects.create(
            user=user,
            title=data['title'],
            date_of_birth=data['date_of_birth'],
        )

        customer.save()

        return redirect('/auth')
        
    return render(request, 'auth/register.html')

# Representative Login View
def representative_login(request):
    if request.method == 'POST':
        user = authenticate_account(request)

        if not user:
            return render(request, 'auth/rep.html', {'error': 'Invalid username and or password'})
        
        login2(request, user)

        return HttpResponseRedirect('/')
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    return render(request, 'auth/rep.html')

@login_required(login_url='/auth')
@user_passes_test(lambda user: user.is_cinemamanager)
@csrf_exempt
def create_film(request):
    if request.method != 'POST':
        raise PermissionDenied 

    # Get the form
    form = FilmForm(request.POST, request.FILES)

    # Check if the form is valid
    if not form.is_valid():
        return JsonResponse({'error': form.errors})
    
    # Get the form data
    data = form.cleaned_data
    
    # Create the film
    film = Film.objects.create(
        title=data['title'],
        description=data['description'],
        duration=data['duration'],
        rating=data['rating'],
        image=data['image'],
        trailer=data['trailer']
    )

    film.save()

    return JsonResponse({'success': 'Film created successfully'})

# Logout View - Samuel
def logout(request):
    # Check if the user is authenticated if so, log them out
    if request.user.is_authenticated:
        logout2(request)

    # Redirect to the login page
    return HttpResponseRedirect('/auth')

# Booking system
def showings(request):
    #function to only show certain dates
    #showings = Film.objects.filter(film_date = selected_date)
    return render(request, 'screenings.html')

#Club Rep
def club_account(request):
    return render(request, 'club_account.html')
