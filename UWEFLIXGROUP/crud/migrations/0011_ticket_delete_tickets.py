# Generated by Django 4.1.6 on 2023-05-02 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0010_tickets_is_child'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_child', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crud.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('viewing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.viewing')),
            ],
        ),
        migrations.DeleteModel(
            name='Tickets',
        ),
    ]
