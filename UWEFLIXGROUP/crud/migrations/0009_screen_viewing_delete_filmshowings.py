# Generated by Django 4.1.6 on 2023-05-01 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0008_alter_filmshowings_screen_delete_screen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Viewing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen', models.IntegerField(default=1)),
                ('film_date', models.DateField()),
                ('film_time', models.TimeField()),
                ('ticket_quantity', models.IntegerField(default=150)),
                ('film', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crud.film')),
            ],
        ),
        migrations.DeleteModel(
            name='FilmShowings',
        ),
    ]
