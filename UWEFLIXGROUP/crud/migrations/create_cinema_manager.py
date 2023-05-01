from django.db import migrations, models

def create_default_manager(apps, schema_editor):
		User = apps.get_model('crud', 'User')

		# If manager or admin already exists, do nothing
		if User.objects.filter(username='manager').exists() or User.objects.filter(username='admin').exists():
				return

		User.objects.create(username='manager', email='manager@uweflix.net', password='manager', is_cinemamanager=True)
		User.objects.create_superuser(username='admin', email='admin@uweflix.net', password='admin', is_accountmanager=True)


class Migration(migrations.Migration):
		dependencies = [
				('crud', '0006_tickets_club_user_alter_club_id_and_more'),
		]

		operations = [
				migrations.RunPython(create_default_manager),
		]