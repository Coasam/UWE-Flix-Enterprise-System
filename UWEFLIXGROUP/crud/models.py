from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Extend the User model to add the following fields:
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_accountmanager = models.BooleanField(default=False)
    is_cinemamanager = models.BooleanField(default=False)
    is_clubrepresentative = models.BooleanField(default=False)
    email = models.EmailField()

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length = 50)
    street_num = models.IntegerField()
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8)
    landline_no = models.CharField(max_length=15)
    mobile_no = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=4)
    cc_number = models.CharField(max_length=30, null=True, blank=True)
    cc_exp = models.CharField(max_length=6, null=True, blank=True)

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

class Viewing(models.Model):
   film = models.ForeignKey(Film, default=1, on_delete=models.CASCADE)
   screen = models.IntegerField(default=1)
   film_date = models.DateField()
   film_time = models.TimeField()
   ticket_quantity = models.IntegerField(default=150)
   

class Ticket(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_child = models.BooleanField(default=False)
    viewing = models.ForeignKey(Viewing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

