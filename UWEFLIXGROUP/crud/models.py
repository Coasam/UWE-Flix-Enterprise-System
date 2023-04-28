from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Account Manager Models - Samuel

# Extend the User model to add the following fields:
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_accountmanager = models.BooleanField(default=False)
    is_cinemamanager = models.BooleanField(default=False)
    is_clubrepresentative = models.BooleanField(default=False)
    email = models.EmailField()

class Representative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()

class Club(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length = 50)
    street_num = models.IntegerField()
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8)
    landline_no = models.CharField(max_length=15)
    mobile_no = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class CinemaManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

class AccountManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=4)
    full_name = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    cc_number = models.CharField(max_length=30, null=True, blank=True)
    cc_exp = models.CharField(max_length=6, null=True, blank=True)
    discount = models.FloatField(default=0.00)

    def __str__(self):
        return self.name

class Film(models.Model):
   title = models.CharField(max_length=100)
   rating = models.CharField(choices=(('U', 'U'), ('PG', 'PG'), ('12A', '12A'), ('12', '12'), ('15', '15'), ('18', '18')), max_length=3, default='U')
   duration = models.IntegerField(default=0)
   description = models.CharField(max_length=500, default='No description available')
   image = models.ImageField(upload_to='uploads/films', default='uploads/films/no-img.jpg')
   trailer = models.URLField(default='https://www.youtube.com/watch?v=dQw4w9WgXcQ')

class Screen(models.Model):
   capacity = models.IntegerField(default=0)

class FilmShowings(models.Model):
   movie = models.ForeignKey(Film, default=1, on_delete=models.CASCADE)
   screen = models.ForeignKey(Screen, default=1, on_delete=models.CASCADE)
   film_date = models.DateField()
   ticket_quantity = models.IntegerField(default=150)

class Tickets(models.Model):
    ticketid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2)
    ticket_quantity = models.PositiveIntegerField()
    film_title = models.CharField(max_length=100)
    film_duration = models.IntegerField(default=0)

