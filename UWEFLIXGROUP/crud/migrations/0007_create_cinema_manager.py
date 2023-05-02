from django.db import migrations, models
from django.contrib.auth.hashers import make_password

def create_default_manager(apps, schema_editor):
		User = apps.get_model('crud', 'User')

		# If manager or admin already exists, drop them
		if User.objects.filter(username='manager@uweflix.net').exists() or User.objects.filter(username='admin@uweflix.net').exists():
				# Drop the default manager
				User.objects.filter(username='manager@uweflix.net').delete()
				User.objects.filter(username='admin@uweflix.net').delete()

		User.objects.create(username='manager@uweflix.net', email='manager@uweflix.net', is_cinemamanager=True, password=make_password('manager'))
		User.objects.create(username='admin@uweflix.net', email='admin@uweflix.net', is_accountmanager=True, password=make_password('admin'))


class Migration(migrations.Migration):
		dependencies = [
				('crud', '0006_tickets_club_user_alter_club_id_and_more'),
		]

		operations = [
				migrations.RunPython(create_default_manager),
		]