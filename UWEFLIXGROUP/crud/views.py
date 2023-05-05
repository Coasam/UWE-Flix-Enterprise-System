from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login2, authenticate, logout as logout2
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

from .models import User, Customer, Viewing, Film, Club, Ticket
from .forms import LoginForm, CustomerForm, ClubForm, ViewingForm, FilmForm, CheckoutForm, DateForm

@login_required(login_url='/auth')
def home(request):
    # Load films
    total_films = []
    films = Film.objects.all()
    viewings = Viewing.objects.all()

    return render(request, 'home.html', {'films':  films, 'viewings': viewings})

@login_required(login_url='/auth')
def filmDetailPage(request, id):
    try:
        film_obj = Film.objects.get(id=id)
    except Film.DoesNotExist:
        film_obj = None
    context = {
        'film_obj': film_obj
        }

    return render(request, 'film_detail_page.html', context)

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
            return render(request, 'auth/index.html', {'error': 'Invalid E-Mail or password'})
            return render(request, 'auth/index.html', {'error': 'Invalid username or password'})

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

def register_club(request):
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
            is_clubrepresentative=True
        )

        user.set_password(data['password'])
        user.save()

        # Create Club
        club_rep = Club.objects.create(
            user=user,
            name="None",
            street="None",
            street_num=1,
            city = "None",
            postcode = "None",
            landline_no = "None",
            mobile_no = "None",
            representative = None,
        )

        club_rep.save()

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
def clubDetailPage(request, id):
    try:
        club_obj = Club.objects.get(user_id=id)
    except Club.DoesNotExist:
        club_obj = None
    context = {
        'club_obj': club_obj
        }

    return render(request, 'modals/club_details.html', context)

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
        return JsonResponse({'error': form.errors}, status=400)

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

@login_required(login_url='/auth')
@user_passes_test(lambda user: user.is_cinemamanager)
@csrf_exempt
def create_viewing(request):
    if request.method != 'POST':
        raise PermissionDenied

    # Get the form
    form = ViewingForm(request.POST)

    # Check if the form is valid
    if not form.is_valid():
        return JsonResponse({'error': form.errors}, status=400)

    # Get the form data
    data = form.cleaned_data

    film = Film.objects.get(id=data['film'])
    
    # Create the film
    viewing = Viewing.objects.create(
        film=film,
        film_date=data['film_date'],
        film_time=data['film_time'],
        screen=data['screen'],
        ticket_quantity=data['ticket_quantity']
    )

    viewing.save()

    return JsonResponse({'success': 'Viewing created successfully'})

# Logout View - Samuel
def logout(request):
    # Check if the user is authenticated if so, log them out
    if request.user.is_authenticated:
        logout2(request)

    # Redirect to the login page
    return HttpResponseRedirect('/auth')

# Booking system
def club_showings(request):
    club_ticket_min = 10
    if request.method == 'POST':
        selected_date = request.POST.get('showing_date', None)
        try:
            showings = Viewing.objects.filter(film_date = selected_date)
            avail_showings=showings.filter(ticket_quantity__gte=club_ticket_min)
            context = {'selected_date': selected_date, 'viewings': avail_showings}
            return render(request, 'viewings.html', context)
        except Viewing.DoesNotExist:
                context = {'selected_date': selected_date}
                return render(request, 'viewings.html', context)

def customer_showings(request):
    #function to only show certain dates
    if request.method == 'POST':
        selected_date = request.POST.get('showing_date', None)
        try:
            showings = Viewing.objects.filter(film_date = selected_date)
            context = {'selected_date': selected_date, 'viewings': showings}
            return render(request, 'viewings.html', context)
        except Viewing.DoesNotExist:
                context = {'selected_date': selected_date}
                return render(request, 'viewings.html', context)

#Club Rep
def club_account(request):
    return render(request, 'club_account.html')

@login_required(login_url='/auth')
@user_passes_test(lambda user: user.is_accountmanager)
def account_manager(request):
    users = User.objects.all()
    
    # Count users tickets
    for user in users:
        user.tickets = Ticket.objects.filter(user=user).count()

    return render(request, 'accounts.html', {'users': users})

@login_required(login_url='/auth')
def checkout(request):
    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if not form.is_valid():
            return render(request, 'checkout.html', {'error': f'Invalid form data - {form.errors}'})

        data = form.cleaned_data

        viewing = Viewing.objects.get(id=data['viewing'])

        # Now we create tickets for each quantity
        for _ in range(data['ticket_quantity']):
            customer = None

            if request.user.is_customer:
                customer = Customer.objects.get(user=request.user)

            ticket = Ticket.objects.create(
                viewing=viewing,
                user=request.user,
                customer=customer,
                is_child=False
            )

            ticket.save()

        for _ in range(data['child_tickets']):
            customer = None

            if request.user.is_customer:
                customer = Customer.objects.get(user=request.user)

            ticket = Ticket.objects.create(
                viewing=viewing,
                user=request.user,
                customer=customer,
                is_child=True
            )

            ticket.save()

        return render(request, 'success.html', {'viewing': viewing})
        

    if request.method == 'GET':
        viewing_id = request.GET.get('viewing')
        viewing = Viewing.objects.get(id=viewing_id)

        return render(request, 'checkout.html', {'viewing': viewing})